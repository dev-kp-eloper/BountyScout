import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# Configuration
STATE_FILE = "seen_bounties.json"
MAX_COMMENTS = 25  # Filter out overcrowded threads

# GitHub search queries for active bounty opportunities
SEARCH_QUERIES = [
    'is:issue is:open bounty in:title,body sort:updated-desc',
    'is:issue is:open reward bounty sort:updated-desc',
    'is:issue is:open "paid" "PR" "bounty" sort:updated-desc',
    'is:issue is:open "Opire" bounty sort:updated-desc',
]

BLOCKLIST = [
    "airdrop", "referral", "casino", "gambling", "trading bot",
    "blog post", "article writing", "tutorial proposal", "content creator",
    "phishing", "spam", "scam",
    "honeypot-task", "请先给项目加星标",
]

# Issue titles matching these substrings are meta-notifications, not real bounties.
TITLE_BLOCKLIST = [
    "bounty alert",
    "new opportunit",
    "account recovery",
    "test codex",
]

LABEL_BLOCKLIST = [
    "bounty-alert",
    "honeypot-task",
]

REPO_BLOCKLIST = [
    "SecureBananaLabs/bug-bounty",
    "dev-kp-eloper/bountyscout",
    "greyw0rks/bountyscout",
    "zhangjiayang6835-cyber/ai-research",
    "pypi/support",
]

REPO_SUFFIX_BLOCKLIST = [
    "/bountyscout",
]


def load_seen_bounties():
    """Load previously seen bounty URLs from the state file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except Exception as e:
            print(f"Error loading state file: {e}")
    return set()


def save_seen_bounties(seen_urls):
    """Save the updated list of seen bounty URLs."""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(seen_urls), f, indent=2)
    except Exception as e:
        print(f"Error saving state file: {e}")


def search_github(query, token=None):
    """Fetch search results from GitHub Issues API."""
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


def is_clean_candidate(item):
    """Triage logic to filter out noisy, assigned, closed, or spam tasks."""
    if "pull_request" in item:
        return False
    if item.get("assignees"):
        return False
    if int(item.get("comments", 0)) > MAX_COMMENTS:
        return False

    repo = item.get("repository_url", "").replace("https://api.github.com/repos/", "")
    repo_lower = repo.lower()
    if any(repo_lower == blocked.lower() for blocked in REPO_BLOCKLIST):
        return False
    if any(repo_lower.endswith(suffix) for suffix in REPO_SUFFIX_BLOCKLIST):
        return False

    labels = [label.get("name", "").lower() for label in item.get("labels", [])]
    if any(blocked in labels for blocked in LABEL_BLOCKLIST):
        return False

    title = str(item.get("title", "")).lower()
    body = str(item.get("body", "") or "").lower()

    if any(term in title for term in TITLE_BLOCKLIST):
        return False

    if any(term in title or term in body for term in BLOCKLIST):
        return False

    return True


def send_telegram_notification(token, chat_id, message):
    """Send a notification message via Telegram Bot API."""
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
    """Send a notification message via Discord Webhook."""
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
    """Create an issue in the host repository to trigger a native GitHub alert."""
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
                if is_clean_candidate(item):
                    new_bounties.append({
                        "title": item.get("title"),
                        "url": url,
                        "repo": url.split("/issues/")[0].replace("https://github.com/", ""),
                        "comments": item.get("comments"),
                        "updated_at": item.get("updated_at")
                    })
                    seen_urls.add(url)

    if not new_bounties:
        print("No new bounty opportunities found.")
        return

    count = len(new_bounties)
    plural = "ies" if count != 1 else "y"
    print(f"Discovered {count} NEW bounty opportunit{plural}!")

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    notif_lines = [
        f"🎯 *New Bounty Alert* ({now_str})",
        f"Found {count} new opportunit{plural}:\n"
    ]
    for idx, b in enumerate(new_bounties, start=1):
        notif_lines.append(f"{idx}. *{b['title']}*")
        notif_lines.append(f"   • Repository: `{b['repo']}`")
        notif_lines.append(f"   • Comments: {b['comments']}")
        notif_lines.append(f"   • Link: {b['url']}\n")

    notification_msg = "\n".join(notif_lines)

    if telegram_token and telegram_chat_id:
        send_telegram_notification(telegram_token, telegram_chat_id, notification_msg)

    if discord_webhook:
        discord_msg = notification_msg.replace("•", "-")
        send_discord_notification(discord_webhook, discord_msg)

    create_github_issues = os.environ.get("BOUNTYSCOUT_GITHUB_ISSUES", "1").strip().lower() not in (
        "0", "false", "no", "off",
    )
    if github_token and repo_fullname and create_github_issues:
        issue_title = f"🎯 Bounty Alert: {count} New Opportunit{plural} found"
        issue_body = (
            f"### Active Bounty Scan Results\n\n"
            f"**Scan Time:** {now_str}\n\n"
        )
        for idx, b in enumerate(new_bounties, start=1):
            issue_body += (
                f"#### {idx}. [{b['title']}]({b['url']})\n"
                f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
                f"- **Comments:** {b['comments']}\n"
                f"- **Last Updated:** {b['updated_at']}\n\n"
            )
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    save_seen_bounties(seen_urls)
    print("State saved successfully.")


if __name__ == "__main__":
    main()
