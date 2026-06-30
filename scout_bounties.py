import json
import os
import requests
from datetime import datetime, timezone
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "dev-kp-eloper"
REPO_NAME = "BountyScout"
SEEN_FILE = "seen_bounties.json"
ISSUE_TEMPLATE = """### Active Bounty Scan Results

**Scan Time:** {scan_time}

{bounty_list}
"""

def load_seen_bounties() -> set:
    """Load the set of already seen bounty IDs."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return set(data.get("seen_ids", []))
            except json.JSONDecodeError:
                return set()
    return set()

def save_seen_bounties(seen_ids: set):
    """Save the set of seen bounty IDs to the JSON file."""
    with open(SEEN_FILE, "w") as f:
        json.dump({"seen_ids": list(seen_ids)}, f, indent=2)

def fetch_bounties() -> List[Dict[str, Any]]:
    """
    Fetches open issues from the target repository that match the 'Bounty' label or keyword.
    In a real scenario, this would query a specific bounty board API or search GitHub issues.
    For this fix, we simulate fetching data based on the issue description context.
    """
    # NOTE: Since the issue description shows specific data that seems to be a bug in the 
    # previous output (truncated URLs, weird titles), we will implement a robust fetcher
    # that handles the GitHub API correctly.
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Search for issues with 'bounty' in title or label in the repo
    # Adjust query based on actual repo structure if needed
    query = f"repo:{REPO_OWNER}/{REPO_NAME} is:open label:bounty"
    url = f"https://api.github.com/search/issues?q={query}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        bounties = []
        for item in data.get("items", []):
            bounties.append({
                "id": item["id"],
                "title": item["title"],
                "url": item["html_url"],
                "comments": item["comments"],
                "updated_at": item["updated_at"]
            })
        return bounties
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return []

def format_bounty_list(bounties: List[Dict[str, Any]], seen_ids: set) -> str:
    """Formats the list of bounties into Markdown, filtering out seen ones."""
    if not bounties:
        return "No new bounty opportunities found."

    lines = []
    for i, bounty in enumerate(bounties, 1):
        if bounty["id"] in seen_ids:
            continue
        
        # Ensure title is clean and URL is valid
        title = bounty["title"].replace("\n", " ").strip()
        url = bounty["url"]
        comments = bounty["comments"]
        updated = bounty["updated_at"]
        
        # Format the list item
        lines.append(f"#### {i}. [{title}]({url})")
        lines.append(f"- **Repository:** {bounty['url'].split('/')[3]}/{bounty['url'].split('/')[4]}")
        lines.append(f"- **Comments:** {comments}")
        lines.append(f"- **Last Updated:** {updated}")
        lines.append("") # Empty line for spacing

    return "\n".join(lines)

def main():
    seen_ids = load_seen_bounties()
    bounties = fetch_bounties()
    
    new_bounties_count = 0
    for bounty in bounties:
        if bounty["id"] not in seen_ids:
            new_bounties_count += 1
    
    if new_bounties_count == 0:
        print("No new bounties found.")
        return

    # Update seen IDs
    for bounty in bounties:
        seen_ids.add(bounty["id"])
    save_seen_bounties(seen_ids)

    # Format the report
    scan_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    bounty_list = format_bounty_list(bounties, seen_ids)
    
    # Note: In a real workflow, this would update a specific issue or create a new one.
    # For this script, we print the result to stdout which the GitHub Action can capture.
    report = ISSUE_TEMPLATE.format(scan_time=scan_time, bounty_list=bounty_list)
    
    print(f"Found {new_bounties_count} new opportunities.")
    print(report)

if __name__ == "__main__":
    main()