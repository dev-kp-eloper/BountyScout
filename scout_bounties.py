import json
import requests
from datetime import datetime

# GitHub Search API endpoint
GITHUB_SEARCH_API = "https://api.github.com/search/issues"

# Search query parameters
SEARCH_PARAMS = {
    "q": "is:issue is:open label:bounty",
    "sort": "updated",
    "order": "desc"
}

# Notification settings
NOTIFICATION_METHOD = "github"  # or "telegram"

def get_new_bounties():
    """Fetch new bounty issues from GitHub Search API"""
    response = requests.get(GITHUB_SEARCH_API, params=SEARCH_PARAMS)
    response.raise_for_status()
    return response.json()["items"]

def filter_bounties(bounties):
    """Filter out non-bounty issues and those with too many comments"""
    filtered_bounties = []
    for bounty in bounties:
        if bounty["comments"] > 25:
            continue
        if "bounty" not in bounty["labels"][0]["name"].lower():
            continue
        filtered_bounties.append(bounty)
    return filtered_bounties

def load_seen_bounties():
    """Load seen bounty URLs from file"""
    try:
        with open("seen_bounties.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_seen_bounties(seen_bounties):
    """Save seen bounty URLs to file"""
    with open("seen_bounties.json", "w") as f:
        json.dump(list(seen_bounties), f)

def notify_bounties(bounties):
    """Notify user of new bounties"""
    if NOTIFICATION_METHOD == "github":
        # Create a new GitHub issue with bounty links
        title = "🎯 Bounty Alert: {} New Opportunities Found".format(len(bounties))
        body = "\n".join(["* [{}]({})".format(bounty["title"], bounty["html_url"]) for bounty in bounties])
        response = requests.post(
            "https://api.github.com/repos/{owner}/{repo}/issues".format(
                owner="your-username", repo="your-repo"
            ),
            headers={"Authorization": "Bearer {}".format("your-github-token")},
            json={"title": title, "body": body, "labels": ["bounty-alert"]}
        )
        response.raise_for_status()
    elif NOTIFICATION_METHOD == "telegram":
        # Send a Telegram message with bounty links
        # TODO: implement Telegram notification
        pass

def main():
    new_bounties = get_new_bounties()
    filtered_bounties = filter_bounties(new_bounties)
    seen_bounties = load_seen_bounties()
    new_bounty_urls = [bounty["html_url"] for bounty in filtered_bounties if bounty["html_url"] not in seen_bounties]
    if new_bounty_urls:
        notify_bounties([bounty for bounty in filtered_bounties if bounty["html_url"] in new_bounty_urls])
        seen_bounties.update(new_bounty_urls)
        save_seen_bounties(seen_bounties)

if __name__ == "__main__":
    main()