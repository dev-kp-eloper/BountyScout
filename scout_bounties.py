
import json
import os

# Placeholder for actual bounty fetching logic
def fetch_current_bounties():
    """Simulates fetching current bounties.
    
    In a real scenario, this would scrape a website, query an API, etc.
    To simulate the "5 New Opportunityies found" alert from the issue,
    this function returns exactly 5 unique bounty identifiers for a fresh run
    (assuming seen_bounties.json is initially empty).
    """
    return {
        "bounty_id_alpha",
        "bounty_id_beta",
        "bounty_id_gamma",
        "bounty_id_delta",
        "bounty_id_epsilon"
    }

def load_seen_bounties(file_path):
    """Loads previously seen bounty IDs from a JSON file."""
    if not os.path.exists(file_path):
        return set()
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Warning: {file_path} content is not a list. Starting with an empty set.")
                return set()
            return set(data)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: {file_path} not found or corrupted. Starting with an empty set of seen bounties.")
        return set()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return set()

def save_seen_bounties(file_path, seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    try:
        # Convert set to list for JSON serialization and sort for consistent file output
        with open(file_path, 'w') as f:
            json.dump(sorted(list(seen_bounties)), f, indent=4)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

def main():
    SEEN_BOUNTIES_FILE = 'seen_bounties.json'

    # Load bounties that have already been seen
    seen_bounty_ids = load_seen_bounties(SEEN_BOUNTIES_FILE)

    # Fetch the current list of available bounties
    current_bounty_ids = fetch_current_bounties()

    # Determine which bounties are new
    new_bounty_ids = current_bounty_ids - seen_bounty_ids

    num_new_bounties = len(new_bounty_ids)

    if num_new_bounties > 0:
        # Fix: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found") 
        
        # Update the set of seen bounties and save it
        seen_bounty_ids.update(new_bounty_ids)
        save_seen_bounties(SEEN_BOUNTIES_FILE, seen_bounty_ids)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {num_new_bounties} new bounties.")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    