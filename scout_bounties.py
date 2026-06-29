import json
import os
import requests
from datetime import datetime
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "dev-kp-eloper"
REPO_NAME = "BountyScout"
SEEN_FILE = "seen_bounties.json"
OUTPUT_FILE = "bounty_report.md"

def load_seen_bounties() -> set:
    """Load the set of already processed bounty IDs."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return set(data.get("seen_ids", []))
            except json.JSONDecodeError:
                return set()
    return set()

def save_seen_bounties(seen_ids: set):
    """Save the updated set of processed bounty IDs."""
    with open(SEEN_FILE, "w") as f:
        json.dump({"seen_ids": list(seen_ids)}, f, indent=2)

def fetch_bounties() -> List[Dict[str, Any]]:
    """
    Fetch open issues from the repository that match bounty keywords.
    In a real scenario, this might query external APIs or specific repos.
    For this fix, we simulate fetching based on the issue description context
    or query the current repo for 'bounty' labeled issues if needed.
    
    However, based on the issue description, it seems the script is supposed 
    to scan external repos or a specific list. Since the issue text shows 
    specific external links, we will assume the script needs to handle 
    the parsing of a list of targets or the GitHub API search.
    
    For this specific fix, we will implement a robust search against GitHub API
    to find issues with 'bounty' in the title across the user's watched repos 
    or a specific list, and format them correctly.
    """
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Search query for issues containing 'bounty' in title, open state
    # Limiting to a reasonable number for the demo
    search_query = "type:issue state:open in:title bounty"
    url = f"https://api.github.com/search/issues?q={search_query}&per_page=100"
    
    bounties = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get("items", []):
            bounties.append({
                "title": item["title"],
                "url": item["html_url"],
                "repo": item["repository_url"].split("/")[-2] + "/" + item["repository_url"].split("/")[-1],
                "comments": item["comments"],
                "updated_at": item["updated_at"],
                "id": item["id"]
            })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return []

    return bounties

def generate_report(new_bounties: List[Dict[str, Any]], seen_ids: set) -> str:
    """Generate the markdown report for new bounties."""
    if not new_bounties:
        return "No new bounties found."

    report_lines = [
        "### Active Bounty Scan Results",
        "",
        f"**Scan Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        ""
    ]

    for idx, bounty in enumerate(new_bounties, 1):
        report_lines.append(f"#### {idx}. [{bounty['title']}]({bounty['url']})")
        report_lines.append(f"- **Repository:** {bounty['repo']}")
        report_lines.append(f"- **Comments:** {bounty['comments']}")
        report_lines.append(f"- **Last Updated:** {bounty['updated_at']}")
        report_lines.append("")

    return "\n".join(report_lines)

def main():
    seen_ids = load_seen_bounties()
    all_bounties = fetch_bounties()
    
    new_bounties = []
    updated_seen_ids = set(seen_ids)

    for bounty in all_bounties:
        if bounty["id"] not in seen_ids:
            new_bounties.append(bounty)
            updated_seen_ids.add(bounty["id"])

    if new_bounties:
        report = generate_report(new_bounties, seen_ids)
        print(report)
        
        # Save to file for GitHub Actions to use
        with open(OUTPUT_FILE, "w") as f:
            f.write(report)
            
        # Update seen bounties
        save_seen_bounties(updated_seen_ids)
        
        print(f"\nFound {len(new_bounties)} new bounties. Report saved to {OUTPUT_FILE}")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()