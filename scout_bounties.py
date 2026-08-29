import json
import os
import urllib.request
import urllib.parse
import re
from datetime import datetime, timezone

# Configuration
STATE_FILE = "seen_bounties.json"
MAX_COMMENTS = 25 # Filter out overcrowded threads

# GitHub search queries for active bounty opportunities
SEARCH_QUERIES = [
    'is:issue is:open bounty in:title,body sort:updated-desc',
    'is:issue is:open reward bounty sort:updated-desc',
    'is:issue is:open "paid" "PR" "bounty" sort:updated-desc',
    'is:issue is:open "Opire" bounty sort:updated-desc',
]

def pluralize_opportunity(count: int, capitalize: bool = False) -> str:
    """Return grammatically correct opportunity/opportunities string."""
    if count == 1:
        return "Opportunity" if capitalize else "opportunity"
    return "Opportunities" if capitalize else "opportunities"

def load_seen_bounties(state_file: str = STATE_FILE):
    """Load previously seen bounty URLs from the state file."""
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except Exception as e:
            print(f"Error loading state file: {e}")
    return set()

def save_seen_bounties(seen_urls, state_file: str = STATE_FILE):
    """Save the updated list of seen bounty URLs."""
    try:
        with open(state_file, "w", encoding="utf-8") as f:
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

def is_clean_candidate(item, current_repo=None):
    """Triage logic to filter out noisy, assigned, closed, spam, or self-referential alert tasks."""
    if not isinstance(item, dict):
        return False

    # 1. Skip if already a Pull Request
    if "pull_request" in item:
        return False

    # 2. Skip if closed or locked
    if item.get("state") == "closed" or item.get("locked") is True:
        return False

    # 3. Skip if already assigned
    if item.get("assignees") or item.get("assignee"):
        return False

    # 4. Skip if thread is overcrowded (highly competitive)
    try:
        if int(item.get("comments", 0)) > MAX_COMMENTS:
            return False
    except (ValueError, TypeError):
        pass

    url = str(item.get("html_url", ""))
    title = str(item.get("title", "")).lower()
    body = str(item.get("body", "")).lower()

    # 5. Skip self-referential alerts, BountyScout repos, and alert loops
    if current_repo and current_repo.lower() in url.lower():
        return False

    if "bountyscout" in url.lower():
        return False

    # Check title for alert patterns
    alert_patterns = [
        "bounty alert:",
        "🎯 bounty alert",
        "new opportunityies found",
        "new opportunities found",
    ]
    if any(p in title for p in alert_patterns):
        return False

    # Check issue labels if present
    labels = item.get("labels", [])
    if isinstance(labels, list):
        for label in labels:
            label_name = (label.get("name", "") if isinstance(label, dict) else str(label)).lower()
            if label_name in ["bounty-alert", "alert", "automated-alert"]:
                return False

    # 6. Skip cryptocurrency/article writing/spam keywords
    blocklist = [
        "airdrop", "referral", "casino", "gambling", "trading bot", 
        "blog post", "article writing", "tutorial proposal", "content creator",
        "faucet", "giveaway", "retweet", "telegram bot", "pump and dump"
    ]
    if any(term in title or term in body for term in blocklist):
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

def format_notification_message(bounties, scan_time_str):
    """Format Telegram/Discord notification message."""
    opp_str = pluralize_opportunity(len(bounties), capitalize=False)
    notif_lines = [
        f"🎯 *New Bounty Alert* ({scan_time_str})",
        f"Found {len(bounties)} new {opp_str}:\n"
    ]
    for idx, b in enumerate(bounties, start=1):
        notif_lines.append(f"{idx}. *{b['title']}*")
        notif_lines.append(f"   • Repository: `{b['repo']}`")
        notif_lines.append(f"   • Comments: {b['comments']}")
        notif_lines.append(f"   • Link: {b['url']}\n")
    return "\n".join(notif_lines)

def build_notification_markdown(bounties, scan_time_str):
    """Alias for format_notification_message."""
    return format_notification_message(bounties, scan_time_str)

def format_github_issue_content(bounties, scan_time_str):
    """Format GitHub Issue title and body."""
    opp_str = pluralize_opportunity(len(bounties), capitalize=True)
    issue_title = f"🎯 Bounty Alert: {len(bounties)} New {opp_str} found"
    issue_body = (
        f"### Active Bounty Scan Results\n\n"
        f"**Scan Time:** {scan_time_str}\n\n"
    )
    for idx, b in enumerate(bounties, start=1):
        issue_body += (
            f"#### {idx}. [{b['title']}]({b['url']})\n"
            f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
            f"- **Comments:** {b['comments']}\n"
            f"- **Last Updated:** {b.get('updated_at', '')}\n\n"
        )
    return issue_title, issue_body

def build_github_issue_payload(bounties, scan_time_str):
    """Alias for format_github_issue_content."""
    return format_github_issue_content(bounties, scan_time_str)

def main():
    # Load credentials/secrets from environment variables
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_fullname = os.environ.get("GITHUB_REPOSITORY") # e.g. "username/my-bounty-tracker"
    
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    seen_urls = load_seen_bounties()
    new_bounties = []

    # Run scouting queries
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
                        "comments": item.get("comments"),
                        "updated_at": item.get("updated_at")
                    })
                    seen_urls.add(url)

    if not new_bounties:
        print("No new bounty opportunities found.")
        return

    print(f"Discovered {len(new_bounties)} NEW bounty opportunities!")

    # Format notification message
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    # 1. Telegram / Discord Message Format (Markdown)
    notification_msg = format_notification_message(new_bounties, now_str)

    # Trigger configured notifications
    
    # Method A: Telegram
    if telegram_token and telegram_chat_id:
        send_telegram_notification(telegram_token, telegram_chat_id, notification_msg)
        
    # Method B: Discord
    if discord_webhook:
        # Convert markdown slightly for Discord compatibility if needed
        discord_msg = notification_msg.replace("•", "-")
        send_discord_notification(discord_webhook, discord_msg)

    # Method C: GitHub Issue (Built-in, zero configuration)
    if github_token and repo_fullname:
        issue_title, issue_body = format_github_issue_content(new_bounties, now_str)
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    # Save state to prevent duplicate notifications
    save_seen_bounties(seen_urls)
    print("State saved successfully.")

if __name__ == "__main__":
    main()
