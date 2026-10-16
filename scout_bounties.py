import json
import os
import urllib.request
import urllib.parse
import re
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

def load_seen_bounties():
    """Load previously seen bounty URLs from the state file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Handle cases where JSON is a list (new) or dict (legacy)
                if isinstance(data, list):
                    return set(data)
                elif isinstance(data, dict):
                    return set(data.get("urls", []))
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
    # Normalize query if needed, e.g. ensure it doesn't break URL encoding
    safe_query = urllib.parse.quote(query, safe=' /')
    url = f"https://api.github.com/search/issues?{urllib.parse.urlencode({'q': safe_query, 'per_page': 100})}"
    
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
    # GitHub Search API returns 'pull_request' key for PRs
    if item.get("pull_request"):
        return False
    
    # 2. Skip if already assigned
    # item.get('assignees') returns a list if not empty, or None
    if item.get("assignees"):
        return False
        
    # 3. Skip if thread is overcrowded (highly competitive)
    comments_count = int(item.get("comments", 0))
    if comments_count > MAX_COMMENTS:
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
            # Optionally log the response content for debugging
            if response.read():
                print("Discord notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")

def collect_and_notify_bounties(token=None, chat_id=None, discord_webhook=None, telegram=True, discord=True):
    """Main driver logic to orchestrate the bounty hunt."""
    seen_bounties = load_seen_bounties()
    
    all_results = {}
    
    for query in SEARCH_QUERIES:
        results = search_github(query, token)
        if results and 'items' in results:
            all_results[query] = results['items']
            
            for item in results['items']:
                # Triage the item
                if is_clean_candidate(item):
                    bounty_url = item.get('html_url', '')
                    title = item.get('title', 'Untitled')
                    
                    if bounty_url not in seen_bounties:
                        seen_bounties.add(bounty_url)
                        
                        # Print console log
                        print(f"\n--- {title} ---\n{bounty_url}")
                    
                    # Notify Discord
                    if discord and discord_webhook:
                        send_discord_notification(discord_webhook, f"*{title}*\n{bounty_url}")
                    
                    # Notify Telegram
                    if telegram and chat_id:
                        send_telegram_notification(telegram, chat_id, f"*{title}*\n{bounty_url}")
    
    # Update the state file with all newly seen items
    save_seen_bounties(seen_bounties)

if __name__ == "__main__":
    # Simple run if no specific args passed
    seen = load_seen_bounties()
    seen.add("https://github.com/Movalabs-crew/mova-store/issues/68") # Example seed
    
    # Run the collector
    collect_and_notify_bounties(
        token="YOUR_GITHUB_TOKEN", # Optional
        chat_id="YOUR_CHAT_ID",    # Optional
        discord_webhook="YOUR_WEBHOOK" # Optional
    )
    
    print(f"Total unique bounties tracked: {len(load_seen_bounties())}")