import os
import requests
from datetime import datetime

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO_OWNER = "dev-kp-eloper"
GITHUB_REPO_NAME = "BountyScout"

def get_bounties():
    # Simulate fetching bounties
    # In a real scenario, this would involve scraping or API calls to bounty platforms
    print("Scanning for bounties...")
    # Using a simplified list for demonstration, matching the structure of the issue body
    bounties = [
        {"title": "[Bounty proposal] fix(mcp): category ValueError exception details in memories and conversations endpoints ($50 proposed)", "repo": "BasedHardware/omi", "comments": 4, "updated_at": "2026-09-28T00:22:53Z", "url": "https://github.com/BasedHardware/omi/issues/18780"},
        {"title": "Railway 赏金：有 5 条值得抢", "repo": "HCTDIP/corps-jobs", "comments": 0, "updated_at": "2026-09-27T23:59:08Z", "url": "https://github.com/HCTDIP/corps-jobs/issues/9"},
        {"title": "Database-less Reconstruction: Indexer-Only State", "repo": "IcanBENCHurCAT/algo-bounty", "comments": 0, "updated_at": "2026-09-27T23:57:08Z", "url": "https://github.com/IcanBENCHurCAT/algo-bounty/issues/183"},
        {"title": "Gateway Address: Central Point of Failure - Multiple Gateway Registry", "repo": "IcanBENCHurCAT/algo-bounty", "comments": 0, "updated_at": "2026-09-27T23:57:06Z", "url": "https://github.com/IcanBENCHurCAT/algo-bounty/issues/184"},
        {"title": "GOV-BURNIN-FREEZE-01 — Garde-fou constitutionnel de l’epoch burn-in active", "repo": "3a7i3/crypto-ia-terminal", "comments": 2, "updated_at": "2026-09-27T23:56:50Z", "url": "https://github.com/3a7i3/crypto-ia-terminal/issues/286"},
        {"title": "AGENT-ECON-00 — Économie d’agents, Bounty Market et amélioration autonome gouvernée", "repo": "3a7i3/crypto-ia-terminal", "comments": 2, "updated_at": "2026-09-27T23:56:48Z", "url": "https://github.com/3a7i3/crypto-ia-terminal/issues/284"},
        {"title": "WEB-DIR-01-D5B — Governed OperatorDecision producer architecture", "repo": "3a7i3/crypto-ia-terminal", "comments": 0, "updated_at": "2026-09-27T23:56:29Z", "url": "https://github.com/3a7i3/crypto-ia-terminal/issues/310"},
        {"title": "Critical Vulrenabilities Need urgent attention", "repo": "ShinnAsukha/oxware-hypervisor", "comments": 0, "updated_at": "2026-09-27T23:39:49Z", "url": "https://github.com/ShinnAsukha/oxware-hypervisor/issues/18"},
        {"title": "[Bounty Proposal] fix(migrations): level migrations exceed Firestore's 500-write batch limit ($25-50 proposed)", "repo": "BasedHardware/omi", "comments": 0, "updated_at": "2026-09-27T23:27:51Z", "url": "https://github.com/BasedHardware/omi/issues/19494"},
        {"title": "[Bounty Proposal] fix(chat): malformed stored messages 500 the initial-message and voice paths ($50 proposed)", "repo": "BasedHardware/omi", "comments": 0, "updated_at": "2026-09-27T23:23:06Z", "url": "https://github.com/BasedHardware/omi/issues/19490"},
        {"title": "[Bounty proposal] fix(developer): category ValueError exceptio", "repo": "BasedHardware/omi", "comments": 0, "updated_at": "2026-09-27T23:23:00Z", "url": "https://github.com/BasedHardware/omi/issues/19491"},
        {"title": "[Bounty proposal] fix(developer): another category ValueError exceptio", "repo": "BasedHardware/omi", "comments": 0, "updated_at": "2026-09-27T23:22:00Z", "url": "https://github.com/BasedHardware/omi/issues/19492"}
    ]
    print(f"Found {len(bounties)} bounties.")
    return bounties

def format_bounty_details(bounties):
    details = []
    for i, bounty in enumerate(bounties):
        details.append(f"#### {i+1}. [{bounty['title']}]({bounty['url']})")
        details.append(f"- **Repository:** [{bounty['repo']}](https://github.com/{bounty['repo']})")
        details.append(f"- **Comments:** {bounty['comments']}")
        details.append(f"- **Last Updated:** {bounty['updated_at']}")
        details.append("")
    return "\n".join(details)

def create_github_issue(title, body):
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set. Cannot create GitHub issue.")
        return

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues"
    data = {
        "title": title,
        "body": body
    }

    print(f"Creating GitHub issue with title: {title}")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Successfully created issue: {response.json()['html_url']}")
    else:
        print(f"Failed to create issue: {response.status_code} - {response.json()}")

def main():
    bounties = get_bounties()
    if bounties:
        scan_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        
        issue_title = f"🎯 Bounty Alert: {len(bounties)} New Opportunities found"
        
        issue_body = f"""### Active Bounty Scan Results

**Scan Time:** {scan_time}

{format_bounty_details(bounties)}
"""
        create_github_issue(issue_title, issue_body)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
