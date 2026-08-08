
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounty IDs from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle case where file is empty or malformed
                return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real application, this would involve web scraping or API calls.
    """
    # Simulate some existing bounties and some new ones
    return {
        "bounty_id_1",
        "bounty_id_2",
        "bounty_id_3",
        "bounty_id_4",
        "bounty_id_5",
        "bounty_id_6",
        "bounty_id_7",
        "bounty_id_8",
        "bounty_id_9",
        "bounty_id_10",
        "bounty_id_11",
        "bounty_id_12",
        "bounty_id_13", # Example new bounty
        "bounty_id_14", # Another example new bounty
    }

def scout_bounties():
    """
    Scouts for new bounties by comparing current bounties with
    previously seen ones and alerts if new opportunities are found.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        count = len(new_bounties)
        # FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {count} New Opportunities found") 
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    