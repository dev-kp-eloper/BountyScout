import json
import requests
from datetime import datetime

# GitHub Search API endpoint
GITHUB_SEARCH_API = "https://api.github.com/search/issues"

# Define search keywords
SEARCH_KEYWORDS = ["bounty", "reward", "paid issue"]

# Define filters
FILTERS = {
    "state": "open",
    "labels": "bounty"
}

# Define notification methods
NOTIFICATION_METHODS = {
    "github_issues": True,
    "telegram": False
}

def get_new_bounties():
    # Get current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load seen bounties from file
    try:
        with open("seen_bounties.json", "r") as f:
            seen_bounties = json.load(f)
    except FileNotFoundError:
        seen_bounties = []

    # Initialize new bounties list
    new_bounties = []

    # Iterate over search keywords
    for keyword in SEARCH_KEYWORDS:
        # Construct search query
        query = f"{keyword} {FILTERS['state']} {FILTERS['labels']}"

        # Send search request to GitHub API
        response = requests.get(GITHUB_SEARCH_API, params={
            "q": query,
            "per_page": 100
        })

        # Check if response was successful
        if response.status_code == 200:
            # Get search results
            results = response.json()["items"]

            # Iterate over search results
            for result in results:
                # Check if result is not already seen
                if result["html_url"] not in seen_bounties:
                    # Add result to new bounties list
                    new_bounties.append({
                        "title": result["title"],
                        "url": result["html_url"],
                        "repository": result["repository_url"],
                        "comments": result["comments"],
                        "updated_at": result["updated_at"]
                    })

                    # Add result to seen bounties list
                    seen_bounties.append(result["html_url"])

    # Save updated seen bounties list to file
    with open("seen_bounties.json", "w") as f:
        json.dump(seen_bounties, f)

    return new_bounties

def send_notifications(new_bounties):
    # Check if there are new bounties
    if new_bounties:
        # Send notifications using chosen method
        if NOTIFICATION_METHODS["github_issues"]:
            # Create new GitHub issue
            title = "🎯 Bounty Alert: {} New Opportunities found".format(len(new_bounties))
            body = "## Issue: 🎯 Bounty Alert\n\n### Active Bounty Scan Results\n\n"
            for bounty in new_bounties:
                body += "- **{}**: [{}]({})\n".format(bounty["title"], bounty["title"], bounty["url"])
            # Use GitHub API to create new issue
            response = requests.post("https://api.github.com/repos/charles-openclaw/charles-microbounties/issues", json={
                "title": title,
                "body": body,
                "labels": ["bounty-alert"]
            }, headers={
                "Authorization": "Bearer {}".format("GITHUB_TOKEN")
            })
            # Check if response was successful
            if response.status_code == 201:
                print("Notification sent successfully!")
            else:
                print("Error sending notification: {}".format(response.text))

def main():
    new_bounties = get_new_bounties()
    send_notifications(new_bounties)

if __name__ == "__main__":
    main()