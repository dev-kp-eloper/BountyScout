
import json
import os
import requests # Assuming 'requests' library is used for fetching bounties
import time

# --- Configuration ---
SEEN_BOUNTIES_FILE = 'seen_bounties.json'
# IMPORTANT: Replace with the actual URL where bounties are fetched from.
# Example: "https://api.github.com/repos/org/repo/issues?labels=bounty"
BOUNTY_SOURCE_URL = "https://api.example.com/bounties" 
# IMPORTANT: This key must match a unique identifier in each bounty object (e.g., 'url', 'id').
# If bounties are just strings (e.g., URLs), set UNIQUE_ID_KEY = None.
UNIQUE_ID_KEY = 'url' 

# --- Helper Functions ---
def load_seen_bounties():
    """
    Loads previously seen bounty unique identifiers from the JSON file.
    Handles file not found, JSON decoding errors, and ensures the loaded data is a list.
    Returns a set of seen bounty identifiers.
    """
    if not os.path.exists(SEEN_BOUNTIES_FILE):
        print(f"Info: {SEEN_BOUNTIES_FILE} not found. Starting with an empty set of seen bounties.")
        return set()
    try:
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            seen_ids_list = json.load(f)
            if not isinstance(seen_ids_list, list):
                print(f"Warning: Content of '{SEEN_BOUNTIES_FILE}' is not a list. Resetting seen bounties.")
                return set()
            return set(seen_ids_list)
    except json.JSONDecodeError as e:
        print(f"Error decoding '{SEEN_BOUNTIES_FILE}': {e}. Resetting seen bounties.")
        return set()
    except Exception as e:
        print(f"An unexpected error occurred loading '{SEEN_BOUNTIES_FILE}': {e}. Resetting seen bounties.")
        return set()

def save_seen_bounties(seen_bounty_ids):
    """
    Saves the current set of seen bounty unique identifiers to the JSON file.
    Converts the set to a list for JSON serialization.
    """
    try:
        with open(SEEN_BOUNTIES_FILE, 'w') as f:
            json.dump(list(seen_bounty_ids), f, indent=2)
    except Exception as e:
        print(f"Error saving '{SEEN_BOUNTIES_FILE}': {e}")

def fetch_current_bounties():
    """
    Fetches the latest bounties from the configured source URL.
    Handles network errors and JSON decoding errors.
    Returns a list of bounty dictionaries or an empty list on failure.
    """
    try:
        response = requests.get(BOUNTY_SOURCE_URL, timeout=15) # Increased timeout
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        bounties = response.json()
        if not isinstance(bounties, list):
            print(f"Warning: Bounty source did not return a list. Received type: {type(bounties)}. Returning empty list.")
            return []
        return bounties
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties from {BOUNTY_SOURCE_URL}: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding bounty response JSON from {BOUNTY_SOURCE_URL}: {e}")
        return []

def get_bounty_identifier(bounty):
    """
    Extracts the unique identifier from a bounty object.
    If UNIQUE_ID_KEY is None, assumes the bounty object itself is the identifier (e.g., a URL string).
    """
    if UNIQUE_ID_KEY is None:
        return bounty # Assume bounty itself is the identifier (e.g., a simple string URL)
    
    if isinstance(bounty, dict):
        return bounty.get(UNIQUE_ID_KEY)
    
    print(f"Warning: Bounty object is not a dictionary and UNIQUE_ID_KEY is set. Cannot extract identifier from: {bounty}")
    return None

# --- Main Logic ---
def main():
    print("Starting bounty scout...")
    seen_bounty_ids = load_seen_bounties()
    print(f"Loaded {len(seen_bounty_ids)} previously seen bounties.")

    current_bounties = fetch_current_bounties()
    if not current_bounties:
        print("Could not fetch current bounties or no bounties available. Exiting.")
        return

    current_bounty_identifiers = set()
    for bounty in current_bounties:
        bounty_id = get_bounty_identifier(bounty)
        if bounty_id:
            current_bounty_identifiers.add(bounty_id)
        else:
            print(f"Warning: A bounty object is missing the unique identifier '{UNIQUE_ID_KEY}' (or is not a dict if '{UNIQUE_ID_KEY}' is set): {bounty}")

    # Identify truly new bounties by comparing current with seen
    new_bounty_ids = current_bounty_identifiers - seen_bounty_ids

    if new_bounty_ids:
        # Fix the typo 'Opportunityies' -> 'Opportunities'
        print(f"🎯 Bounty Alert: {len(new_bounty_ids)} New Opportunities found")
        
        # Optionally, print details of new bounties
        for bounty_id in new_bounty_ids:
            # Try to find the original bounty data for more context
            new_bounty_data = next((b for b in current_bounties if get_bounty_identifier(b) == bounty_id), None)
            if new_bounty_data and isinstance(new_bounty_data, dict):
                # Assuming common keys like 'title' or 'name' exist
                print(f"  - {new_bounty_data.get('title', new_bounty_data.get('name', bounty_id))}")
            else:
                print(f"  - {bounty_id}")

        # Update seen bounties with the newly found ones
        seen_bounty_ids.update(new_bounty_ids)
        save_seen_bounties(seen_bounty_ids)
        print(f"Successfully updated '{SEEN_BOUNTIES_FILE}'. Total seen bounties: {len(seen_bounty_ids)}")
    else:
        print("No new bounties found this run.")

if __name__ == "__main__":
    main()
    