
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounties that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounties to the file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real scenario, this would involve scraping a website,
    calling an API, or reading from a database to get the latest bounties.
    For demonstration, it returns a hardcoded set of bounties.
    """
    # Example: Simulating 14 new bounties for the alert message
    # In a real application, this would be dynamic.
    return {f"bounty_{i:02d}" for i in range(1, 15)} # Simulates 14 bounties

def scout_for_bounties():
    """
    Checks for new bounties by comparing current bounties with
    previously seen bounties and generates an alert if new ones are found.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_bounties()
    