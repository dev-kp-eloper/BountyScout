
import json
import os
import requests
from datetime import datetime

# Configuration
SEEN_BOUNTIES_FILE = 'seen_bounties.json'
# Placeholder URL for bounty source. Replace with actual API/scrape target.
BOUNTY_SOURCE_URL = 'https://example.com/api/bounties' 

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    # Convert set to list for JSON serialization
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    """Fetches current bounties from the source URL."""
    try:
        response = requests.get(BOUNTY_SOURCE_URL, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        bounties_data = response.json()
        
        current_bounty_ids = set()
        # Assuming bounties_data is a list of dictionaries, each representing a bounty.
        # We try to extract a unique identifier like 'id' or 'url'.
        for bounty in bounties_data:
            if isinstance(bounty, dict):
                if 'id' in bounty:
                    current_bounty_ids.add(str(bounty['id']))
                elif 'url' in bounty: # Fallback if 'id' is not present
                    current_bounty_ids.add(str(bounty['url']))
                # Add more logic here to extract unique IDs based on actual API response structure
        return current_bounty_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties from {BOUNTY_SOURCE_URL}: {e}")
        return set()
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {BOUNTY_SOURCE_URL}. Received non-JSON response.")
        return set()
    except Exception as e:
        print(f"An unexpected error occurred during bounty fetching: {e}")
        return set()

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting bounty scout...")
    
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    if not current_bounties:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Could not retrieve any current bounties. Exiting.")
        return

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") 
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {len(new_bounties)} new bounties saved to {SEEN_BOUNTIES_FILE}.")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No new bounties found.")

if __name__ == "__main__":
    main()
    