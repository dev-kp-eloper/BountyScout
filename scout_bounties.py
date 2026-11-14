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
    'is:issue is:open "Algora" bounty sort:updated-desc',
    'is:issue is:open "polar.sh" bounty sort:updated-desc',
]

# Hanzo.ai track: same query that powers https://hanzo.ai/bounty
HANZO_QUERIES = [
    'is:issue is:open label:bounty archived:false org:hanzoai org:hanzo-apps org:hanzo-go org:hanzo-js',
]

HANZO_ORGS = {"hanzoai", "hanzo-apps", "hanzo-go", "hanzo-js", "hanzo-inc", "hanzo-dev"}
PAID_SOURCES = {"algora", "opire", "polar"}

# Labels applied to digest issues (created automatically on first run)
LABELS = {
    "bounty-alert": {"color": "F9D0C4", "description": "New bounty opportunities found by scout"},
    "hanzo": {"color": "1D76DB", "description": "Hanzo.ai bounty (AI credits + leaderboard points)"},
    "paid": {"color": "0E8A16", "description": "Bounty with a cash/crypto payout"},
}

AMOUNT_RE = re.compile(r"\$\s?(\d[\d,]*)")

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
    body = str(item.get("body") or "").lower()
    
    # 4. Skip cryptocurrency/article writing/spam keywords
    blocklist = [
        "airdrop", "referral", "casino", "gambling", "trading bot", 
        "blog post", "article writing", "tutorial proposal", "content creator"
    ]
    if any(term in title or term in body for term in blocklist):
        return False
        
    return True

def detect_source(item):
    """Classify a bounty by its track: hanzo, a paid platform, or generic."""
    url = item.get("html_url", "")
    owner = url.split("/")[3].lower() if url.startswith("https://github.com/") else ""
    if owner in HANZO_ORGS:
        return "hanzo"
    text = f"{item.get('title', '')} {item.get('body') or ''}".lower()
    if "algora" in text or "/bounty" in text:
        return "algora"
    if "opire" in text:
        return "opire"
    if "polar.sh" in text or "polar" in text:
        return "polar"
    return "generic"

def extract_amount(item):
    """Pull the largest $ amount mentioned in the title/body, if any."""
    text = f"{item.get('title', '')} {item.get('body') or ''}"
    amounts = [int(m.replace(",", "")) for m in AMOUNT_RE.findall(text)]
    return max(amounts) if amounts else None

def reward_label(bounty):
    """Human-readable reward line for a bounty."""
    if bounty["source"] == "hanzo":
        return "+100-500 pts + $20 AI credits"
    if bounty.get("amount"):
        return f"~${bounty['amount']:,}"
    if bounty["source"] in PAID_SOURCES:
        return f"via {bounty['source'].capitalize()}"
    return "Unspecified"

def bounty_sort_key(bounty):
    """Hanzo first, then priced bounties (largest first), then everything else."""
    tier = 0 if bounty["source"] == "hanzo" else (1 if bounty.get("amount") else 2)
    return (tier, -(bounty.get("amount") or 0))

def build_devin_command(bounty):
    """Generate a copy-paste devin --cloud command for a single bounty."""
    num = bounty["url"].rsplit("/", 1)[-1]
    prompt = (
        f"Attempt this bounty: {bounty['url']} "
        f"1) Use gh to fork {bounty['repo']} to my account and clone the fork. "
        f"2) Create a branch and implement the fix described in the issue. "
        f"3) Run the repo's tests or a relevant check. "
        f"4) Push the branch to my fork and open an upstream PR with 'Fixes #{num}' "
        f"in the body, plus a one-line note that the fix was AI-assisted. "
        f"Do not post comments on the issue."
    )
    # For Hanzo bounties you may prepend: comment "Taking this" on the issue first.
    return f'devin --cloud -p "{prompt}"'

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

def ensure_labels(repo_fullname, token):
    """Create digest labels idempotently (fresh forks don't have them)."""
    url = f"https://api.github.com/repos/{repo_fullname}/labels"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    for name, meta in LABELS.items():
        payload = {"name": name, "color": meta["color"], "description": meta["description"]}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15):
                print(f"Created label '{name}'.")
        except urllib.error.HTTPError as e:
            if e.code == 422:
                continue # Label already exists
            print(f"Failed to create label '{name}': {e}")
        except Exception as e:
            print(f"Failed to create label '{name}': {e}")

def create_github_issue(repo_fullname, token, title, body, labels):
    """Create an issue in the host repository to trigger a native GitHub alert."""
    url = f"https://api.github.com/repos/{repo_fullname}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": labels
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
    repo_fullname = os.environ.get("GITHUB_REPOSITORY") # e.g. "username/my-bounty-tracker"
    
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    seen_urls = load_seen_bounties()
    new_bounties = []

    # Run scouting queries (Hanzo track first so its results are never starved)
    print("Scouting GitHub for active bounties...")
    for query in HANZO_QUERIES + SEARCH_QUERIES:
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
                        "updated_at": item.get("updated_at"),
                        "source": detect_source(item),
                        "amount": extract_amount(item),
                    })
                    seen_urls.add(url)

    if not new_bounties:
        print("No new bounty opportunities found.")
        return

    new_bounties.sort(key=bounty_sort_key)
    print(f"Discovered {len(new_bounties)} NEW bounty opportunities!")

    # Format notification message
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    # 1. Telegram / Discord Message Format (Markdown)
    notif_lines = [
        f"🎯 *New Bounty Alert* ({now_str})",
        f"Found {len(new_bounties)} new opportunity{'ies' if len(new_bounties) > 1 else ''}:\n"
    ]
    for idx, b in enumerate(new_bounties, start=1):
        notif_lines.append(f"{idx}. *{b['title']}*")
        notif_lines.append(f"   • Repository: `{b['repo']}`")
        notif_lines.append(f"   • Source: `{b['source']}` | Reward: {reward_label(b)}")
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
        ensure_labels(repo_fullname, github_token)
        issue_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunity{'ies' if len(new_bounties) > 1 else ''} found"
        issue_body = (
            f"### Active Bounty Scan Results\n\n"
            f"**Scan Time:** {now_str}\n\n"
            f"Pick a bounty, copy its `devin` command into your terminal, and let Devin ship the fix.\n\n"
        )
        sources = {b["source"] for b in new_bounties}
        issue_labels = ["bounty-alert"]
        if "hanzo" in sources:
            issue_labels.append("hanzo")
        if sources & PAID_SOURCES or any(b.get("amount") for b in new_bounties):
            issue_labels.append("paid")
        for idx, b in enumerate(new_bounties, start=1):
            issue_body += (
                f"#### {idx}. [{b['title']}]({b['url']})\n"
                f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
                f"- **Source:** `{b['source']}` · **Reward:** {reward_label(b)}\n"
                f"- **Comments:** {b['comments']} · **Last Updated:** {b['updated_at']}\n"
                f"\n```bash\n{build_devin_command(b)}\n```\n\n"
            )
        create_github_issue(repo_fullname, github_token, issue_title, issue_body, issue_labels)

    # Save state to prevent duplicate notifications
    save_seen_bounties(seen_urls)
    print("State saved successfully.")

if __name__ == "__main__":
    main()
