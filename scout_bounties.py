import json
import os
import requests
from datetime import datetime, timezone
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPOS_TO_SCAN = [
    "Scottcjn/rustchain-bounties",
    "Scottcjn/Rustchain",
    # Add more repos as needed
]
SEEN_FILE = "seen_bounties.json"
OUTPUT_FILE = "bounty_report.md"

def load_seen_bounties() -> set:
    """Load the set of already seen issue IDs."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            try:
                data = json.load(f)
                return set(data.get("seen_ids", []))
            except json.JSONDecodeError:
                return set()
    return set()

def save_seen_bounties(seen_ids: set):
    """Save the updated set of seen issue IDs."""
    with open(SEEN_FILE, "w") as f:
        json.dump({"seen_ids": list(seen_ids)}, f, indent=2)

def fetch_bounties() -> List[Dict[str, Any]]:
    """Fetch open issues that look like bounties from configured repos."""
    bounties = []
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    for repo in REPOS_TO_SCAN:
        url = f"https://api.github.com/repos/{repo}/issues"
        params = {
            "state": "open",
            "labels": "bounty", # Assuming a label exists, or we filter by title
            "per_page": 100
        }
        
        # Fallback if no label strategy is defined, just fetch open issues and filter
        if not GITHUB_TOKEN:
            print("Warning: No GITHUB_TOKEN provided. Rate limits may apply.")

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            issues = response.json()
            
            for issue in issues:
                # Simple heuristic: Check if title contains "Bounty" or "Reward"
                # Or check if the repo is known to be a bounty repo
                if "bounty" in issue["title"].lower() or "reward" in issue["title"].lower() or "opportunity" in issue["title"].lower():
                    bounties.append({
                        "title": issue["title"],
                        "url": issue["html_url"],
                        "repo": repo,
                        "comments": issue["comments"],
                        "updated_at": issue["updated_at"],
                        "number": issue["number"]
                    })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues for {repo}: {e}")
            continue

    return bounties

def generate_report(new_bounties: List[Dict[str, Any]]) -> str:
    """Generate a markdown report of new bounties."""
    if not new_bounties:
        return "No new bounties found."

    scan_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    report = f"### Active Bounty Scan Results\n\n"
    report += f"**Scan Time:** {scan_time}\n\n"
    
    for i, bounty in enumerate(new_bounties, 1):
        report += f"#### {i}. [{bounty['title']}]({bounty['url']})\n"
        report += f"- **Repository:** [{bounty['repo']}](https://github.com/{bounty['repo']})\n"
        report += f"- **Comments:** {bounty['comments']}\n"
        report += f"- **Last Updated:** {bounty['updated_at']}\n\n"

    return report

def main():
    seen_ids = load_seen_bounties()
    all_bounties = fetch_bounties()
    
    new_bounties = []
    current_seen_ids = set()

    for bounty in all_bounties:
        issue_id = f"{bounty['repo']}#{bounty['number']}"
        current_seen_ids.add(issue_id)
        
        if issue_id not in seen_ids:
            new_bounties.append(bounty)

    # Update seen set
    seen_ids.update(current_seen_ids)
    save_seen_bounties(seen_ids)

    if new_bounties:
        report = generate_report(new_bounties)
        print(f"Found {len(new_bounties)} new bounties!")
        print(report)
        
        # Optional: Save to file
        with open(OUTPUT_FILE, "w") as f:
            f.write(report)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()