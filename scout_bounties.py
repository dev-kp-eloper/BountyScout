import requests
import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "BountyScout/1.0"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# File to track seen bounties to avoid duplicates
SEEN_FILE = "seen_bounties.json"

def load_seen_bounties() -> set:
    """Load the set of already seen bounty URLs."""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r") as f:
                data = json.load(f)
                return set(data.get("seen_urls", []))
        except (json.JSONDecodeError, IOError):
            return set()
    return set()

def save_seen_bounties(seen_urls: set):
    """Save the updated set of seen bounties."""
    with open(SEEN_FILE, "w") as f:
        json.dump({"seen_urls": list(seen_urls)}, f, indent=2)

def fetch_bounties() -> List[Dict[str, Any]]:
    """
    Fetches open issues from target repositories that match bounty criteria.
    This is a simplified example. In a real scenario, you would query specific
    repos or use a search query like 'is:issue is:open label:bounty'.
    """
    # Example search query for bounty-related issues
    query = "is:issue is:open label:bounty OR label:opportunity"
    url = f"https://api.github.com/search/issues?q={query}&sort=updated&order=desc"
    
    bounties = []
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get("items", []):
            # Basic validation to ensure it looks like a bounty
            if "bounty" in item.get("labels", []).__str__().lower() or "opportunity" in item.get("labels", []).__str__().lower():
                bounties.append({
                    "title": item.get("title", "Untitled"),
                    "url": item.get("html_url", ""),
                    "repo": item.get("repository_url", "").split("/")[-1], # Simplified repo name
                    "comments": item.get("comments", 0),
                    "updated_at": item.get("updated_at", ""),
                    "repository_full": item.get("repository_url", "").replace("https://api.github.com/repos/", "")
                })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from GitHub API")
        return []
        
    return bounties

def format_report(new_bounties: List[Dict[str, Any]]) -> str:
    """Formats the list of new bounties into a markdown report."""
    if not new_bounties:
        return "No new bounties found."

    scan_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    count = len(new_bounties)
    
    # Fixed typo: Opportunityies -> Opportunities
    header = f"### Active Bounty Scan Results\n\n**Scan Time:** {scan_time}\n\n"
    
    body = ""
    for i, bounty in enumerate(new_bounties, 1):
        # Ensure we handle missing fields gracefully
        title = bounty.get("title", "Unknown Title")
        url = bounty.get("url", "#")
        repo = bounty.get("repository_full", "Unknown Repo")
        comments = bounty.get("comments", 0)
        updated = bounty.get("updated_at", "Unknown")
        
        # Truncate long titles if necessary, but ensure no broken lines
        if len(title) > 80:
            title = title[:77] + "..."
            
        body += f"#### {i}. [{title}]({url})\n"
        body += f"- **Repository:** [{repo}]({url.split('/issues')[0]})\n"
        body += f"- **Comments:** {comments}\n"
        body += f"- **Last Updated:** {updated}\n\n"

    return header + body

def main():
    print("Starting Bounty Scout scan...")
    
    seen_urls = load_seen_bounties()
    all_bounties = fetch_bounties()
    
    new_bounties = []
    for bounty in all_bounties:
        url = bounty.get("url")
        if url and url not in seen_urls:
            new_bounties.append(bounty)
            seen_urls.add(url)
    
    if new_bounties:
        report = format_report(new_bounties)
        print(f"\n{report}")
        
        # Save the new URLs to avoid reporting them again
        save_seen_bounties(seen_urls)
        
        # In a real CI/CD context, this might post to a GitHub Issue or Slack
        # For now, we just print the count
        print(f"\n✅ Scan complete. {len(new_bounties)} new opportunities found.")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()