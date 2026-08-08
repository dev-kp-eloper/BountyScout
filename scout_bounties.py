
import json
import requests
import time
import os

# --- Configuration ---
# These can be moved to a separate config file or environment variables for better management.
# Using a placeholder URL. In a real scenario, this would point to a bounty source (e.g., GitHub API).
BOUNTY_SOURCE_URL = os.environ.get("BOUNTY_SOURCE_URL", "https://api.github.com/repos/example/bounties/issues")
SEEN_BOUNTIES_FILE = "seen_bounties.json"
REQUEST_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    # Uncomment and configure if authentication is required or rate limits need to be bypassed
    # "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}"
}

def load_seen_bounties():
    """
    Loads a set of bounty IDs that have been seen before from the SEEN_BOUNTIES_FILE.
    Returns an empty set if the file does not exist or cannot be parsed.
    """
    if not os.path.exists(SEEN_BOUNTIES_FILE):
        return set()
    try:
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            return set(json.load(f))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Could not load or parse {SEEN_BOUNTIES_FILE}: {e}. Starting with an empty set of seen bounties.")
        return set()

def save_seen_bounties(bounties_set):
    """
    Saves the current set of seen bounty IDs to the SEEN_BOUNTIES_FILE in JSON format.
    """
    try:
        with open(SEEN_BOUNTIES_FILE, 'w') as f:
            json.dump(list(bounties_set), f, indent=2)
    except IOError as e:
        print(f"Error saving seen bounties to {SEEN_BOUNTIES_FILE}: {e}")

def fetch_current_bounties():
    """
    Fetches current bounties from the configured BOUNTY_SOURCE_URL.
    Assumes the response is a JSON list of objects, each with an 'id' field.
    Returns a set of unique bounty IDs.
    """
    print(f"Fetching bounties from {BOUNTY_SOURCE_URL}...")
    try:
        response = requests.get(BOUNTY_SOURCE_URL, headers=REQUEST_HEADERS)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Assuming 'data' is a list of bounties, and each bounty has a unique identifier 'id'
        current_bounty_ids = {item['id'] for item in data if isinstance(item, dict) and 'id' in item}
        print(f"Found {len(current_bounty_ids)} current bounties.")
        return current_bounty_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties from {BOUNTY_SOURCE_URL}: {e}")
        return set()
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {BOUNTY_SOURCE_URL}. Response might not be valid JSON.")
        return set()

def scout_bounties():
    """
    Main function to scout for new bounties, identify new opportunities,
    alert the user, and update the list of seen bounties.
    """
    seen_bounty_ids = load_seen_bounties()
    current_bounty_ids = fetch_current_bounties()

    # Identify new bounties by comparing current bounties with previously seen ones
    new_bounty_ids = current_bounty_ids - seen_bounty_ids

    if new_bounty_ids:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounty_ids)} New Opportunities found")
        # Update seen bounties: union with all current bounties to ensure
        # that even if a bounty was removed and re-added, it's still considered seen.
        updated_seen_bounty_ids = seen_bounty_ids.union(current_bounty_ids)
        save_seen_bounties(updated_seen_bounty_ids)
    else:
        print("No new bounties found.")
    print("Scouting complete.")

if __name__ == "__main__":
    scout_bounties()
    