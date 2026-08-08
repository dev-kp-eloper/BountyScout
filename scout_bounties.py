
import json
import requests
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'
# Placeholder URL - in a real scenario, this would point to a bounty source API
BOUNTY_SOURCE_URL = 'https://api.github.com/repos/octocat/Spoon-Knife/issues' # Example: GitHub issues as 'bounties'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=4)

def fetch_current_bounties():
    """Fetches current bounties from a source (e.g., an API)."""
    try:
        response = requests.get(BOUNTY_SOURCE_URL)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Assuming bounties are represented by items with unique 'id' fields
        # This example uses GitHub issues and their 'id'
        current_bounty_ids = set()
        for item in response.json():
            if 'id' in item:
                current_bounty_ids.add(item['id'])
        return current_bounty_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties from {BOUNTY_SOURCE_URL}: {e}")
        return set()

def main():
    """Main function to scout for new bounties."""
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL CHANGE: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") 
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
