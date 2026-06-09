import json
import requests
from datetime import datetime

# GitHub Search API endpoint
GITHUB_SEARCH_API = "https://api.github.com/search/issues"

# Bounty search keywords
BOUNTY_KEYWORDS = ["bounty", "reward", "opportunity"]

# Maximum number of comments to consider a thread as "overcrowded"
MAX_COMMENTS = 25

# Crypto-related keywords to filter out
CRYPTO_KEYWORDS = ["crypto", "bitcoin", "ethereum"]

def get_github_token():
    # Use the built-in GITHUB_TOKEN environment variable
    return os.environ["GITHUB_TOKEN"]

def search_github(query):
    # Set up the API request headers
    headers = {
        "Authorization": f"Bearer {get_github_token()}",
        "Content-Type": "application/json"
    }

    # Set up the API request parameters
    params = {
        "q": query,
        "sort": "updated",
        "order": "desc"
    }

    # Send the API request
    response = requests.get(GITHUB_SEARCH_API, headers=headers, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Error searching GitHub: {response.status_code}")
        return []

def triage_candidates(candidates):
    # Filter out pull requests, already-assigned issues, overcrowded threads, and crypto-related spam
    filtered_candidates = []
    for candidate in candidates:
        if candidate["pull_request"] or candidate["assignee"] or candidate["comments"] > MAX_COMMENTS:
            continue
        if any(crypto_keyword in candidate["title"].lower() for crypto_keyword in CRYPTO_KEYWORDS):
            continue
        filtered_candidates.append(candidate)
    return filtered_candidates

def get_seen_bounties():
    try:
        with open("seen_bounties.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_seen_bounties(seen_bounties):
    with open("seen_bounties.json", "w") as file:
        json.dump(seen_bounties, file)

def notify_new_bounties(new_bounties):
    # Create a new GitHub issue with the bounty links
    issue_title = "🎯 Bounty Alert: {} New Opportunities Found".format(len(new_bounties))
    issue_body = "The following new bounties were found:\n\n"
    for bounty in new_bounties:
        issue_body += "- [{}]({})\n".format(bounty["title"], bounty["html_url"])
    issue_labels = ["bounty-alert"]

    # Use the GitHub API to create a new issue
    headers = {
        "Authorization": f"Bearer {get_github_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "title": issue_title,
        "body": issue_body,
        "labels": issue_labels
    }
    response = requests.post("https://api.github.com/repos/{}/{}/issues".format(os.environ["GITHUB_REPOSITORY_OWNER"], os.environ["GITHUB_REPOSITORY"]), headers=headers, json=data)

    # Check if the issue was created successfully
    if response.status_code == 201:
        print("New bounty alert issue created successfully")
    else:
        print("Error creating new bounty alert issue: {}".format(response.status_code))

def main():
    # Search for new bounties
    query = " ".join(BOUNTY_KEYWORDS)
    candidates = search_github(query)

    # Triage the candidates
    filtered_candidates = triage_candidates(candidates)

    # Get the seen bounties
    seen_bounties = get_seen_bounties()

    # Find new bounties
    new_bounties = [bounty for bounty in filtered_candidates if bounty["html_url"] not in seen_bounties]

    # Notify about new bounties
    if new_bounties:
        notify_new_bounties(new_bounties)

    # Save the updated seen bounties
    seen_bounties.extend([bounty["html_url"] for bounty in new_bounties])
    save_seen_bounties(seen_bounties)

if __name__ == "__main__":
    main()