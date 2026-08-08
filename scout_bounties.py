
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed or empty, starting with an empty set of seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def scout_bounties():
    """
    Simulates scouting for new bounties, identifies new opportunities,
    and prints an alert. Updates the list of seen bounties.
    """
    seen_bounties = load_seen_bounties()

    # Simulate finding new bounties from an external source.
    # In a real application, this would involve web scraping or API calls.
    # We create 15 unique bounty IDs to match the issue description's "15 New Opportunities".
    current_found_bounties = {f"bounty_id_{i:02d}" for i in range(1, 16)} # Example: bounty_id_01 ... bounty_id_15

    # Determine which bounties are truly new (not in seen_bounties)
    new_bounties = current_found_bounties - seen_bounties

    new_bounties_count = len(new_bounties)

    if new_bounties_count > 0:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunities found")
    else:
        print("No new bounties found.")

    # Update the set of seen bounties with all currently found bounties
    seen_bounties.update(current_found_bounties)
    save_seen_bounties(seen_bounties)

if __name__ == "__main__":
    # Example usage:
    # 1. Run the script: It will report 15 new bounties and save them to seen_bounties.json.
    # 2. Run it again: It will report 0 new bounties because they are now "seen".
    # To reset for testing, manually delete the seen_bounties.json file.
    scout_bounties()
    