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

if __name__ == "__main__":
    # Load initial state
    seen_bounties = load_seen_bounties()
    all_results = []
    
    # Iterate through search queries to aggregate results
    for query in SEARCH_QUERIES:
        results = search_github(query)
        if results and "items" in results:
            for item in results["items"]:
                if is_clean_candidate(item):
                    all_results.append(item)
                    seen_bounties.add(item["html_url"])
            
            # Save state periodically to avoid bloating memory if querying many times
            save_seen_bounties(seen_bounties)
            
    # Format the message if we have results
    if all_results:
        now = datetime.now(timezone.utc)
        message = f"🎯 Bounty Alert: {len(all_results)} New Opportunities found\n"
        message += "### Active Bounty Scan Results\n\n**Scan Time:** " + now.strftime("%Y-%m-%d %H:%M UTC")
        message += "\n\n"
        
        for i, item in enumerate(all_results, 1):
            title = item.get("title", "Untitled")
            repo = item.get("repository", {})
            repo_link = repo.get("html_url", "#")
            comments = item.get("comments", 0)
            updated = item.get("updated_at", "")
            
            message += f"#### {i}. [{title}]({item.get('html_url')})\n"
            message += f"- **Repository:** [{repo.get('name')}]({repo_link})\n"
            message += f"- **Comments:** {comments}\n"
            message += f"- **Last Updated:** {updated}\n\n"

        # Send the final notification (using Discord as the primary in this context)
        discord_webhook = os.environ.get("DISCORD_WEBHOOK", "")
        if discord_webhook:
            send_discord_notification(discord_webhook, message)
        else:
            # Fallback to Telegram or print if no webhook provided
            telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID", "123456789")
            if telegram_token and chat_id:
                send_telegram_notification(telegram_token, chat_id, message)

    else:
        message = "🎯 No new bounties found!"
        if discord_webhook:
            send_discord_notification(discord_webhook, message)