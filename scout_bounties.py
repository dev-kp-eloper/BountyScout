import requests
import json

def fetch_bounties(repo, headers):
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {
        "state": "open",
        "labels": "bounty"
    }
    issues = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            issues.extend(response.json())
            # Check if there's a next page
            url = response.links.get('next', {}).get('url')
            if url:
                # If there's a next page, remove the params from the url
                # as they are already included in the params dictionary
                url = url.split('{?state,labels}')[0]
        else:
            print(f"Failed to fetch issues from {repo}: {response.status_code}")
            break
    return issues

def main():
    token = "your_github_token_here"  # Replace with your actual GitHub token
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    repos = ["charles-openclaw/charles-microbounties"]  # List of repositories to scan
    
    seen_bounties = set()
    try:
        with open('seen_bounties.json', 'r') as f:
            seen_bounties = set(json.load(f))
    except FileNotFoundError:
        pass
    
    new_bounties = []
    for repo in repos:
        issues = fetch_bounties(repo, headers)
        for issue in issues:
            issue_url = issue['html_url']
            if issue_url not in seen_bounties:
                new_bounties.append({
                    "repository": repo,
                    "url": issue_url,
                    "comments": issue['comments'],
                    "last_updated": issue['updated_at']
                })
                seen_bounties.add(issue_url)
    
    # Save the seen bounties to the JSON file
    with open('seen_bounties.json', 'w') as f:
        json.dump(list(seen_bounties), f)
    
    # Process new bounties (e.g., print them or trigger an alert)
    if new_bounties:
        print(f"Found {len(new_bounties)} new bounty opportunities:")
        for bounty in new_bounties:
            print(f"- {bounty['url']}")

if __name__ == "__main__":
    main()