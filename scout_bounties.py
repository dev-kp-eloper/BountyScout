
import json
import requests
import os
import time

# Configuration
# This URL is an example. In a real scenario, this would point to a bounty platform API.
BOUNTY_API_URL = os.getenv("BOUNTY_API_URL", "https://api.github.com/repos/octocat/Spoon-Knife/issues")
SEEN_BOUNTIES_FILE = "seen_bounties.json"
# GITHUB_TOKEN is used for authenticated requests to avoid rate limits on GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def load_seen_bounties(filename):
    """Loads previously seen bounty IDs from a JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                # Load existing IDs, ensuring it's a set for efficient lookup
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {filename} is corrupted or empty. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(filename, bounties):
    """Saves current bounty IDs to a JSON file."""
    # Convert set to list for JSON serialization
    with open(filename, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_bounties(url, token=None):
    """Fetches bounty IDs from the specified URL."""
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        
        # Assuming the API returns a list of dictionaries, each with an 'id' field
        bounties_data = response.json()
        # Extract unique IDs from the fetched data
        return {item.get('id') for item in bounties_data if item.get('id')}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties from {url}: {e}")
        return set()

def main():
    print("Scouting for new bounties...")
    seen_bounties = load_seen_bounties(SEEN_BOUNTIES_FILE)
    current_bounty_ids = fetch_bounties(BOUNTY_API_URL, GITHUB_TOKEN)

    # Determine new bounties by finding IDs present in current but not in seen
    new_bounties = current_bounty_ids - seen_bounties

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        
        # Add new bounties to the seen list and save
        seen_bounties.update(new_bounties)
        save_seen_bounties(SEEN_BOUNTIES_FILE, seen_bounties)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {len(new_bounties)} new bounties.")
    else:
        print("No new bounties found this round.")

if __name__ == "__main__":
    main()
    