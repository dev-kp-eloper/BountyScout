
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of seen bounty identifiers from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle cases where the JSON file might be malformed
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty identifiers to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    """
    Simulates fetching current bounty identifiers.
    In a real application, this would involve web scraping or API calls.
    For this example, it returns a static list of identifiers.
    
    To simulate "1 New Opportunity found":
    1. Ensure `seen_bounties.json` is empty or contains fewer bounties than returned here.
    2. Adjust the returned list to yield exactly one new bounty when compared
       with the `seen_bounties.json` content.
    Example: if `seen_bounties.json` is empty, returning `['bounty_id_1']` would trigger
    the "1 New Opportunity found" message. Returning `['bounty_id_1', 'bounty_id_2']`
    would trigger "2 New Opportunities found".
    """
    return ["bounty_id_1", "bounty_id_2", "bounty_id_3"]

def scout_for_bounties():
    """
    Main function to scout for new bounties, compare with seen ones,
    alert about new opportunities, and update the seen bounties list.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = set(fetch_current_bounties())

    new_bounties = current_bounties - seen_bounties
    
    new_bounties_count = len(new_bounties)

    if new_bounties_count > 0:
        # --- START MODIFICATION ---
        # Generate a precise alert message based on the count of new bounties
        if new_bounties_count == 1:
            print("🎯 Bounty Alert: 1 New Opportunity found")
        else:
            print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunities found")
        # --- END MODIFICATION ---
        
        # Add newly found bounties to the seen list
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_bounties()
    