import json
import os
import requests
from datetime import datetime, timezone
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "BountyScout"
}

if GITHUB_TOKEN:
    headers = {**HEADERS, "Authorization": f"token {GITHUB_TOKEN}"}
else:
    headers = HEADERS

SEEN_FILE = "seen_bounties.json"
OUTPUT_FILE = "bounty_report.md"

def load_seen_bounties() -> set:
    """Load the set of already seen issue URLs."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("seen_urls", []))
    return set()

def save_seen_bounties(seen_urls: set):
    """Save the updated set of seen issue URLs."""
    with open(SEEN_FILE, "w") as f:
        json.dump({"seen_urls": list(seen_urls)}, f, indent=2)

def fetch_issues(owner: str, repo: str, state: str = "open") -> List[Dict[str, Any]]:
    """Fetch open issues from a specific GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": 100,
        "sort": "updated",
        "direction": "desc"
    }
    
    issues = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues for {owner}/{repo}: {e}")
    
    return issues

def scan_bounties() -> List[Dict[str, Any]]:
    """
    Scan specific repositories for new bounty opportunities.
    In a real scenario, this list would be dynamic or loaded from a config.
    Based on the issue description, we are scanning for 'okalldal/lark'.
    """
    # Target repositories to scan
    targets = [
        {"owner": "okalldal", "repo": "lark"},
        # Add more repositories here as needed
    ]
    
    seen_urls = load_seen_bounties()
    new_bounties = []
    
    print(f"Starting scan at {datetime.now(timezone.utc).isoformat()}")
    
    for target in targets:
        owner = target["owner"]
        repo = target["repo"]
        print(f"Scanning {owner}/{repo}...")
        
        issues = fetch_issues(owner, repo)
        
        for issue in issues:
            # Skip pull requests (GitHub API returns PRs in issues endpoint)
            if "pull_request" in issue:
                continue
            
            issue_url = issue["html_url"]
            
            if issue_url not in seen_urls:
                new_bounties.append({
                    "title": issue["title"],
                    "url": issue_url,
                    "repository": f"{owner}/{repo}",
                    "comments": issue["comments"],
                    "updated_at": issue["updated_at"],
                    "labels": [label["name"] for label in issue.get("labels", [])]
                })
                seen_urls.add(issue_url)
    
    # Update the seen list
    save_seen_bounties(seen_urls)
    
    return new_bounties

def generate_report(bounties: List[Dict[str, Any]]) -> str:
    """Generate a markdown report of the new bounties."""
    if not bounties:
        return "No new bounties found."
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    report = f"""### Active Bounty Scan Results

**Scan Time:** {timestamp}

"""
    
    for i, bounty in enumerate(bounties, 1):
        # Extract severity from title if present (e.g., [medium])
        severity = "Unknown"
        for label in bounty["labels"]:
            if label.startswith("[") and label.endswith("]"):
                severity = label.strip("[]")
                break
        # Fallback to title parsing if label not found
        if severity == "Unknown" and bounty["title"].startswith("["):
            parts = bounty["title"].split("]")
            if len(parts) > 0:
                severity = parts[0].strip("[").strip()

        report += f"#### {i}. [[{severity}] {bounty['title']}]\n"
        report += f"- **Repository:** [{bounty['repository']}](https://github.com/{bounty['repository']})\n"
        report += f"- **Comments:** {bounty['comments']}\n"
        report += f"- **Last Updated:** {bounty['updated_at']}\n\n"
        
    return report

def main():
    new_bounties = scan_bounties()
    
    if new_bounties:
        report = generate_report(new_bounties)
        print(report)
        
        # Save report to file
        with open(OUTPUT_FILE, "w") as f:
            f.write(report)
            
        print(f"\nFound {len(new_bounties)} new bounties. Report saved to {OUTPUT_FILE}")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()