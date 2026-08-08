
import json
import requests
import os

# Constants for file paths
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def fetch_bounties():
    # Placeholder for actual bounty fetching logic
    # In a real scenario, this would involve API calls, parsing, etc.
    # This function should return a list of bounty dictionaries,
    # where each dictionary has at least an 'id' key.
    
    # Example simulation:
    # return [
    #     {"id": "bounty_id_1", "title": "First Bounty"},
    #     {"id": "bounty_id_2", "title": "Second Bounty"},
    # ]
    # For the purpose of this issue, we assume this function works correctly
    # and provides the current set of bounties.
    
    # Returning an empty list for now, as actual implementation is unknown
    # and we want to preserve existing functionality.
    return [] 

def load_seen_bounties():
    if not os.path.exists(SEEN_BOUNTIES_FILE):
        return set()
    try:
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(data)
            else:
                print(f"Warning: {SEEN_BOUNTIES_FILE} content is not a list of IDs. Starting fresh.")
                return set()
    except json.JSONDecodeError:
        print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting fresh.")
        return set()
    except Exception as e:
        print(f"Error loading {SEEN_BOUNTIES_FILE}: {e}. Starting fresh.")
        return set()

def save_seen_bounties(seen_ids):
    try:
        with open(SEEN_BOUNTIES_FILE, 'w') as f:
            json.dump(list(seen_ids), f, indent=2) # Use indent for readability
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to save {SEEN_BOUNTIES_FILE}: {e}")
        # Re-raise the exception to indicate a critical failure in persistence
        raise

def main():
    current_bounties = fetch_bounties()
    current_bounty_ids = {b['id'] for b in current_bounties}

    seen_bounty_ids = load_seen_bounties()

    new_bounty_ids = current_bounty_ids - seen_bounty_ids

    if new_bounty_ids:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounty_ids)} New Opportunities found")

        # Update and save seen bounties
        seen_bounty_ids.update(new_bounty_ids)
        try:
            save_seen_bounties(seen_bounty_ids)
        except Exception:
            # If saving fails, print an informative message and exit gracefully
            print("Persistence failed. The issue 'New Opportunities found' might recur due to save failure.")
            return

        # NEW: Post-persistence verification step
        # This acts as an internal test to ensure newly found bounties are actually persisted.
        reloaded_seen_bounty_ids = load_seen_bounties()
        if not new_bounty_ids.issubset(reloaded_seen_bounty_ids):
            print("CRITICAL VERIFICATION ERROR: Newly found bounties were NOT correctly persisted to seen_bounties.json after saving!")
            print("This indicates a serious problem with the save/load mechanism, causing recurring alerts.")
        else:
            print(f"Verification successful: {len(new_bounty_ids)} new bounties confirmed persisted.")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    