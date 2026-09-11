"""Automated GitHub bounty scanner and multi-channel notification dispatcher."""

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

SPAM_BLOCKLIST = [
    "airdrop",
    "referral",
    "casino",
    "gambling",
    "trading bot",
    "blog post",
    "article writing",
    "tutorial proposal",
    "content creator",
    "faucet",
    "giveaway",
]


def load_seen_bounties(filepath=STATE_FILE):
    """Load previously seen bounty URLs from the JSON state file.

    Args:
        filepath (str): Path to the state JSON file. Defaults to STATE_FILE.

    Returns:
        set: A set of URL strings that have been previously processed.
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
    """Save the updated set of seen bounty URLs to the JSON state file.

    Args:
        seen_urls (set or list): Collection of seen issue URL strings.
        filepath (str): Path to the target JSON state file. Defaults to STATE_FILE.

    Returns:
        None
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sorted(list(seen_urls)), f, indent=2)
    except Exception as e:
        print(f"Error saving state file {filepath}: {e}")


def search_github(query, token=None):
    """Fetch search results from GitHub Issues API.

    Args:
        query (str): The search query string.
        token (str, optional): GitHub personal access token or action token.

    Returns:
        dict: The parsed JSON response dictionary from the GitHub Search API.
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
    """Triage logic to filter out noisy, assigned, closed, spam, or recursive alert issues.

    Args:
        item (dict): Issue item dictionary returned by the GitHub API.
        current_repo (str, optional): The current host repository 'owner/repo' to avoid self-scraping.

    Returns:
        bool: True if the issue is a valid, clean bounty candidate; False otherwise.
    """
    if not isinstance(item, dict):
        return False

    if "pull_request" in item and item["pull_request"]:
        return False

    if item.get("state") and item.get("state") != "open":
        return False

    if item.get("locked") is True:
        return False

    if item.get("assignees") or item.get("assignee"):
        return False

    comments_count = item.get("comments")
    if comments_count is not None:
        try:
            if int(comments_count) > MAX_COMMENTS:
                return False
        except (ValueError, TypeError):
            pass

    title = str(item.get("title") or "")
    body = str(item.get("body") or "")
    html_url = str(item.get("html_url") or "")
    title_lower = title.lower()
    body_lower = body.lower()

    if "bounty alert" in title_lower:
        return False

    if "/bountyscout/" in html_url.lower():
        return False

    if current_repo and current_repo.lower() in html_url.lower():
        return False

    for term in SPAM_BLOCKLIST:
        if term in title_lower or term in body_lower:
            return False

    return True


def format_issue_title(count):
    """Format the GitHub issue title with correct singular/plural English grammar.

    Args:
        count (int): Number of newly discovered bounty opportunities.

    Returns:
        str: Formatted issue title string.
    """
    word = "Opportunity" if count == 1 else "Opportunities"
    return f"🎯 Bounty Alert: {count} New {word} found"


def format_issue_body(bounties, now_str):
    """Format the markdown body for the native GitHub issue notification.

    Args:
        bounties (list): List of bounty dictionaries with title, url, repo, comments, updated_at.
        now_str (str): Formatted UTC timestamp string.

    Returns:
        str: Formatted markdown string.
    """
    lines = [
        "### Active Bounty Scan Results\n\n",
        f"**Scan Time:** {now_str}\n\n",
    ]
    for idx, b in enumerate(bounties, start=1):
        lines.append(
            f"#### {idx}. [{b['title']}]({b['url']})\n"
            f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
            f"- **Comments:** {b.get('comments', 0)}\n"
            f"- **Last Updated:** {b.get('updated_at', '')}\n\n"
        )
    return "".join(lines)


def format_notification_message(bounties, now_str):
    """Format Telegram and Discord text notifications with proper grammar.

    Args:
        bounties (list): List of bounty dictionaries.
        now_str (str): Formatted UTC timestamp string.

    Returns:
        str: Notification message string.
    """
    count = len(bounties)
    word = "opportunity" if count == 1 else "opportunities"
    lines = [
        f"🎯 *New Bounty Alert* ({now_str})",
        f"Found {count} new {word}:\n",
    ]
    for idx, b in enumerate(bounties, start=1):
        lines.append(f"{idx}. *{b['title']}*")
        lines.append(f"   • Repository: `{b['repo']}`")
        lines.append(f"   • Comments: {b.get('comments', 0)}")
        lines.append(f"   • Link: {b['url']}\n")
    return "\n".join(lines)


def send_telegram_notification(token, chat_id, message):
    """Send a notification message via Telegram Bot API.

    Args:
        token (str): Telegram Bot token.
        chat_id (str): Telegram target chat or channel ID.
        message (str): Markdown formatted message.

    Returns:
        None
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Telegram notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")


def send_discord_notification(webhook_url, message):
    """Send a notification message via Discord Webhook.

    Args:
        webhook_url (str): Discord webhook URL.
        message (str): Plain or markdown formatted message content.

    Returns:
        None
    """
    payload = {"content": message}
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Discord notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")


def create_github_issue(repo_fullname, token, title, body):
    """Create an issue in the host repository to trigger a native GitHub alert.

    Args:
        repo_fullname (str): Repository full name formatted as 'owner/repo'.
        token (str): GitHub personal access token or Actions GITHUB_TOKEN.
        title (str): Issue title.
        body (str): Issue markdown body.

    Returns:
        None
    """
    url = f"https://api.github.com/repos/{repo_fullname}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": ["bounty-alert"],
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            print("GitHub Issue notification created successfully.")
    except Exception as e:
        print(f"Failed to create GitHub Issue notification: {e}")


def main():
    """Main execution pipeline for scouting bounties and dispatching notifications."""
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_fullname = os.environ.get("GITHUB_REPOSITORY")

    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    seen_urls = load_seen_bounties(STATE_FILE)
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
                        "updated_at": item.get("updated_at", ""),
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

    save_seen_bounties(seen_urls, STATE_FILE)
    print("State saved successfully.")


if __name__ == "__main__":
    main()
