
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have been seen before."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_current_bounties_mock():
    """
    Mocks fetching all current bounties from a source (e.g., an API).
    This list includes some "old" bounties and 14 truly "new" ones
    to simulate the issue's reported count.
    """
    return {
        "old_bounty_1", "old_bounty_2", # These are assumed to be in seen_bounties.json initially
        "new_bounty_1", "new_bounty_2", "new_bounty_3", "new_bounty_4",
        "new_bounty_5", "new_bounty_6", "new_bounty_7", "new_bounty_8",
        "new_bounty_9", "new_bounty_10", "new_bounty_11", "new_bounty_12",
        "new_bounty_13", "new_bounty_14" # These 14 are truly new
    }

def scout_bounties():
    """
    Main function to scout for new bounties, report them, and update
    the list of seen bounties.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties_mock() # Simulate fetching all current bounties

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        # Add new bounties to seen list
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    