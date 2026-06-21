import json
import os
import requests
from datetime import datetime, timezone
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPOS_TO_SCAN = [
    "lissy93/bug-bounties",
    "lobster-trap/Kickama",
    # Add more repositories as needed
]
SEEN_FILE = "seen_bounties.json"
OUTPUT_FILE = "bounty_report.md"

def load_seen_bounties() -> set:
    """Load the set of already seen issue IDs to avoid duplicates."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("seen_ids", []))
    return set()

def save_seen_bounties(seen_ids: set):
    """Save the updated set of seen issue IDs."""
    with open(SEEN_FILE, "w") as f:
        json.dump({"seen_ids": list(seen_ids)}, f, indent=2)

def fetch_bounties(repo: str, seen_ids: set) -> List[Dict[str, Any]]:
    """Fetch open issues from a repository that contain 'bounty' in the title."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {
        "state": "open",
        "per_page": 100,
        "sort": "updated",
        "direction": "desc"
    }
    
    new_bounties = []
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        for issue in issues:
            # Skip pull requests
            if "pull_request" in issue:
                continue
                
            title = issue.get("title", "").lower()
            issue_id = issue.get("number")
            
            # Check if it's a bounty (simple keyword check)
            if "bounty" in title or "reward" in title:
                if issue_id not in seen_ids:
                    new_bounties.append({
                        "title": issue.get("title"),
                        "url": issue.get("html_url"),
                        "repo": repo,
                        "comments": issue.get("comments"),
                        "updated_at": issue.get("updated_at"),
                        "id": issue_id
                    })
                    seen_ids.add(issue_id)
                    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues from {repo}: {e}")
        
    return new_bounties

def generate_report(bounties: List[Dict[str, Any]], scan_time: datetime) -> str:
    """Generate a markdown report of the found bounties."""
    report = []
    report.append("### Active Bounty Scan Results\n")
    report.append(f"**Scan Time:** {scan_time.strftime('%Y-%m-%d %H:%M')} UTC\n")
    report.append(f"**Total New Opportunities:** {len(bounties)}\n")
    report.append("---\n")
    
    if not bounties:
        report.append("No new bounty opportunities found.")
        return "\n".join(report)
    
    for idx, bounty in enumerate(bounties, 1):
        report.append(f"#### {idx}. [{bounty['title']}]({bounty['url']})")
        report.append(f"- **Repository:** [{bounty['repo']}](https://github.com/{bounty['repo']})")
        report.append(f"- **Comments:** {bounty['comments']}")
        report.append(f"- **Last Updated:** {bounty['updated_at']}")
        report.append("")
        
    return "\n".join(report)

def main():
    seen_ids = load_seen_bounties()
    all_new_bounties = []
    
    print(f"Scanning {len(REPOS_TO_SCAN)} repositories...")
    
    for repo in REPOS_TO_SCAN:
        print(f"  Scanning {repo}...")
        bounties = fetch_bounties(repo, seen_ids)
        all_new_bounties.extend(bounties)
    
    scan_time = datetime.now(timezone.utc)
    report = generate_report(all_new_bounties, scan_time)
    
    # Save report to file
    with open(OUTPUT_FILE, "w") as f:
        f.write(report)
    
    # Update seen bounties
    save_seen_bounties(seen_ids)
    
    print(f"Scan complete. Found {len(all_new_bounties)} new opportunities.")
    print(f"Report saved to {OUTPUT_FILE}")
    
    # If running in CI, we might want to print the report to stdout
    print("\n--- Report Content ---\n")
    print(report)

if __name__ == "__main__":
    main()