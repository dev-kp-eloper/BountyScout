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
    'is:issue is:open "polar.sh" bounty sort:updated-desc',
    'is:issue is:open "algora.io" sort:updated-desc',
]

def extract_reward(body, title):
    """Attempt to extract bounty amount from text using common patterns."""
    combined = (title + " " + (body or "")).lower()
    # Patterns: $100, 100$, 100 USD, 100 USDT, 100 USDC, 2.5 SOL, 0.1 ETH
    patterns = [
        r"\$(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*\$",
        r"(\d+(?:\.\d+)?)\s*usd",
        r"(\d+(?:\.\d+)?)\s*usdt",
        r"(\d+(?:\.\d+)?)\s*usdc",
        r"(\d+(?:\.\d+)?)\s*sol",
        r"(\d+(?:\.\d+)?)\s*eth",
    ]
    for p in patterns:
        match = re.search(p, combined)
        if match:
            return match.group(0).upper()
    return None

def search_github(query, token=None):
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

def search_polar(token=None):
    """Fetch funded issues directly from Polar.sh API."""
    url = "https://api.polar.sh/v1/funding/"
    headers = {
        "Accept": "application/json",
        "User-Agent": "MyPersonalBountyScout",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8")).get("items", [])
    except Exception as e:
        print(f"Polar API Error: {e}")
        return []

def is_clean_candidate(item):
    """Triage logic to filter out noisy, assigned, closed, or spam tasks."""
    # 1. Skip if already a Pull Request
    if "pull_request" in item:
        return False
    # 2. Skip if already assigned
    if item.get("assignees"):
        return False
    # 3. Skip if thread is overcrowded (highly competitive)
    if int(item.get("comments", 0)) > MAX_COMMENTS:
        return False
    
    title = str(item.get("title", "")).lower()
    body = str(item.get("body", "")).lower()
    
    # 4. Skip cryptocurrency/article writing/spam keywords
    blocklist = [
        "airdrop", "referral", "casino", "gambling", "trading bot", 
        "blog post", "article writing", "tutorial proposal", "content creator"
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

def main():
    # Load credentials/secrets from environment variables
    github_token = os.environ.get("GITHUB_TOKEN")
    polar_token = os.environ.get("POLAR_ACCESS_TOKEN")
    repo_fullname = os.environ.get("GITHUB_REPOSITORY") # e.g. "username/my-bounty-tracker"
    
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    seen_urls = load_seen_bounties()
    new_bounties = []

    # Method 1: GitHub Search API
    print("Scouting GitHub for active bounties...")
    for query in SEARCH_QUERIES:
        results = search_github(query, github_token)
        for item in results.get("items", []):
            url = item.get("html_url")
            if url and url not in seen_urls:
                if is_clean_candidate(item):
                    reward = extract_reward(item.get("body"), item.get("title"))
                    new_bounties.append({
                        "title": item.get("title"),
                        "url": url,
                        "repo": url.split("/issues/")[0].replace("https://github.com/", ""),
                        "comments": item.get("comments"),
                        "updated_at": item.get("updated_at"),
                        "reward": reward
                    })
                    seen_urls.add(url)

    # Method 2: Polar.sh Funding API
    print("Scouting Polar.sh for funded issues...")
    polar_items = search_polar(polar_token)
    for item in polar_items:
        issue = item.get("issue", {})
        url = issue.get("html_url")
        if url and url not in seen_urls:
            funding = item.get("funding", {}).get("total", {})
            amount = None
            if funding:
                # Polar API returns amount in cents
                amount = f"${funding.get('amount', 0) / 100} {funding.get('currency', '').upper()}"
            
            new_bounties.append({
                "title": issue.get("title"),
                "url": url,
                "repo": url.split("/issues/")[0].replace("https://github.com/", ""),
                "comments": issue.get("comments_count", 0),
                "updated_at": issue.get("updated_at"),
                "reward": amount
            })
            seen_urls.add(url)

    if not new_bounties:
        print("No new bounty opportunities found.")
        return

    print(f"Discovered {len(new_bounties)} NEW bounty opportunities!")

    # Format notification message
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    # 1. Telegram / Discord Message Format (Markdown)
    notif_lines = [
        f"🎯 *New Bounty Alert* ({now_str})",
        f"Found {len(new_bounties)} new opportunit{'ies' if len(new_bounties) > 1 else 'y'}:\n"
    ]
    for idx, b in enumerate(new_bounties, start=1):
        reward_info = f" 💰 *{b['reward']}*" if b.get("reward") else ""
        notif_lines.append(f"{idx}. *{b['title']}*{reward_info}")
        notif_lines.append(f"   • Repository: `{b['repo']}`")
        notif_lines.append(f"   • Comments: {b['comments']}")
        notif_lines.append(f"   • Link: {b['url']}\n")
    
    notification_msg = "\n".join(notif_lines)

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
        issue_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunit{'ies' if len(new_bounties) > 1 else 'y'} found"
        issue_body = (
            f"### Active Bounty Scan Results\n\n"
            f"**Scan Time:** {now_str}\n\n"
        )
        for idx, b in enumerate(new_bounties, start=1):
            reward_info = f" - **Reward:** {b['reward']}" if b.get("reward") else ""
            issue_body += (
                f"#### {idx}. [{b['title']}]({b['url']}){reward_info}\n"
                f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
                f"- **Comments:** {b['comments']}\n"
                f"- **Last Updated:** {b['updated_at']}\n\n"
            )
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    # Save state to prevent duplicate notifications
    save_seen_bounties(seen_urls)
    print("State saved successfully.")

if __name__ == "__main__":
    main()
