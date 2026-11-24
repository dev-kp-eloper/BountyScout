import json
import os
import urllib.request
import urllib.parse
import re
from datetime import datetime, timezone

STATE_FILE = "seen_bounties.json"
MAX_COMMENTS = 25

SEARCH_QUERIES = [
    'is:issue is:open bounty in:title,body sort:updated-desc',
    'is:issue is:open reward bounty sort:updated-desc',
    'is:issue is:open "paid" "PR" "bounty" sort:updated-desc',
    'is:issue is:open "Opire" bounty sort:updated-desc',
]

def load_seen_bounties(filepath=STATE_FILE):
    """
    Load previously seen bounty URLs from the state file.

    :param filepath: Path to the JSON state file.
    :return: Set of seen bounty URL strings.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except Exception as e:
            print(f"Error loading state file {filepath}: {e}")
    return set()

def save_seen_bounties(seen_urls, filepath=STATE_FILE):
    """
    Save the updated list of seen bounty URLs to the state file.

    :param seen_urls: Set or list of seen bounty URL strings.
    :param filepath: Path to the JSON state file.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sorted(list(seen_urls)), f, indent=2)
    except Exception as e:
        print(f"Error saving state file {filepath}: {e}")

def search_github(query, token=None):
    """
    Fetch search results from GitHub Issues API.

    :param query: GitHub search query string.
    :param token: Optional GitHub API personal access token.
    :return: Parsed JSON response dictionary.
    """
    url = f"https://api.github.com/search/issues?{urllib.parse.urlencode({'q': query, 'per_page': 15})}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"GitHub Search API Error for query '{query}': {e}")
        return {}

def is_clean_candidate(item, current_repo=None):
    """
    Evaluate whether a GitHub issue item is a valid, unassigned bounty candidate.

    :param item: Dictionary representing a GitHub issue search result.
    :param current_repo: Optional string of the current repository fullname to avoid self-referencing.
    :return: Boolean indicating if the item is an actionable bounty opportunity.
    """
    if not isinstance(item, dict):
        return False

    if "pull_request" in item:
        return False

    if item.get("state") != "open" or item.get("locked") is True:
        return False

    if item.get("assignee") or item.get("assignees"):
        return False

    comments = item.get("comments", 0)
    if comments is not None and int(comments) > MAX_COMMENTS:
        return False

    title = str(item.get("title") or "").strip()
    body = str(item.get("body") or "").strip()
    html_url = str(item.get("html_url") or "").strip()

    title_lower = title.lower()
    body_lower = body.lower()
    url_lower = html_url.lower()

    if "bounty alert" in title_lower or "/bountyscout" in url_lower:
        return False

    if current_repo and current_repo.lower() in url_lower:
        return False

    blocklist = [
        "airdrop", "referral", "casino", "gambling", "trading bot",
        "blog post", "article writing", "tutorial proposal", "content creator",
        "faucet", "giveaway"
    ]
    if any(term in title_lower or term in body_lower for term in blocklist):
        return False

    return True

def format_issue_title(count):
    """
    Format GitHub issue title with correct singular or plural inflection.

    :param count: Number of discovered bounty opportunities.
    :return: Formatted title string.
    """
    unit = "Opportunity" if count == 1 else "Opportunities"
    return f"🎯 Bounty Alert: {count} New {unit} found"

def format_issue_body(bounties, now_str):
    """
    Format GitHub issue markdown body containing the list of discovered bounties.

    :param bounties: List of bounty dictionaries.
    :param now_str: Formatted UTC timestamp string.
    :return: Markdown body string.
    """
    body_lines = [
        "### Active Bounty Scan Results\n",
        f"**Scan Time:** {now_str}\n"
    ]
    for idx, b in enumerate(bounties, start=1):
        body_lines.append(
            f"#### {idx}. [{b['title']}]({b['url']})\n"
            f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
            f"- **Comments:** {b['comments']}\n"
            f"- **Last Updated:** {b['updated_at']}\n"
        )
    return "\n".join(body_lines)

def format_notification_message(bounties, now_str):
    """
    Format Telegram or Discord notification message with correct singular or plural inflection.

    :param bounties: List of bounty dictionaries.
    :param now_str: Formatted UTC timestamp string.
    :return: Markdown notification text.
    """
    count = len(bounties)
    unit = "opportunity" if count == 1 else "opportunities"
    notif_lines = [
        f"🎯 *New Bounty Alert* ({now_str})",
        f"Found {count} new {unit}:\n"
    ]
    for idx, b in enumerate(bounties, start=1):
        notif_lines.append(f"{idx}. *{b['title']}*")
        notif_lines.append(f"   • Repository: `{b['repo']}`")
        notif_lines.append(f"   • Comments: {b['comments']}")
        notif_lines.append(f"   • Link: {b['url']}\n")
    return "\n".join(notif_lines)

def send_telegram_notification(token, chat_id, message):
    """
    Send a notification message via Telegram Bot API.

    :param token: Telegram Bot Token.
    :param chat_id: Telegram Chat ID.
    :param message: Message text to transmit.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Telegram notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

def send_discord_notification(webhook_url, message):
    """
    Send a notification message via Discord Webhook.

    :param webhook_url: Discord incoming webhook URL.
    :param message: Message payload text.
    """
    payload = {
        "content": message
    }
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Discord notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")

def create_github_issue(repo_fullname, token, title, body):
    """
    Create an issue in the host repository to trigger a native GitHub alert.

    :param repo_fullname: Repository path in 'owner/repo' format.
    :param token: GitHub API token with issue creation permissions.
    :param title: Issue title string.
    :param body: Markdown body of the issue.
    """
    url = f"https://api.github.com/repos/{repo_fullname}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": ["bounty-alert"]
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            print("GitHub Issue notification created successfully.")
    except Exception as e:
        print(f"Failed to create GitHub Issue notification: {e}")

def main():
    """
    Execute bounty scouting pipeline and deliver notifications.
    """
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_fullname = os.environ.get("GITHUB_REPOSITORY")

    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    seen_urls = load_seen_bounties()
    new_bounties = []

    print("Scouting GitHub for active bounties...")
    for query in SEARCH_QUERIES:
        results = search_github(query, github_token)
        for item in results.get("items", []):
            url = item.get("html_url")
            if url and url not in seen_urls:
                if is_clean_candidate(item, current_repo=repo_fullname):
                    new_bounties.append({
                        "title": item.get("title"),
                        "url": url,
                        "repo": url.split("/issues/")[0].replace("https://github.com/", ""),
                        "comments": item.get("comments", 0),
                        "updated_at": item.get("updated_at")
                    })
                    seen_urls.add(url)

    if not new_bounties:
        print("No new bounty opportunities found.")
        return

    print(f"Discovered {len(new_bounties)} NEW bounty opportunities!")

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    notification_msg = format_notification_message(new_bounties, now_str)

    if telegram_token and telegram_chat_id:
        send_telegram_notification(telegram_token, telegram_chat_id, notification_msg)

    if discord_webhook:
        discord_msg = notification_msg.replace("•", "-")
        send_discord_notification(discord_webhook, discord_msg)

    if github_token and repo_fullname:
        issue_title = format_issue_title(len(new_bounties))
        issue_body = format_issue_body(new_bounties, now_str)
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    save_seen_bounties(seen_urls)
    print("State saved successfully.")

if __name__ == "__main__":
    main()
