
import json
import os

# Define the path for storing seen bounties
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with no seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def find_new_bounties():
    """
    Simulates finding new bounties and alerts the user.
    In a real application, this would involve scraping websites or APIs.
    """
    # Placeholder for actual bounty finding logic
    # This set represents all bounties currently available from the source.
    # For demonstration, we'll use a static set.
    all_current_bounties = {
        "bounty_id_001", "bounty_id_002", "bounty_id_003", "bounty_id_004",
        "bounty_id_005", "bounty_id_006", "bounty_id_007", "bounty_id_008",
        "bounty_id_009", "bounty_id_010", "bounty_id_011", "bounty_id_012",
        "bounty_id_013", "bounty_id_014", "bounty_id_015", # Example: more than 13 to show dynamic count
    }

    seen_bounties = load_seen_bounties()
    
    new_bounties = all_current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    find_new_bounties()
    