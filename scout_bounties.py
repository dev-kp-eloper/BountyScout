
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the list of seen bounties from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return []
    return []

def save_seen_bounties(bounties):
    """Saves the current list of bounties to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(bounties, f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching bounties from a source.
    In a real application, this would scrape a website or call an API.
    """
    # Example bounties for demonstration purposes
    return [
        {"id": "bounty1", "title": "Fix login bug", "status": "open"},
        {"id": "bounty2", "title": "Implement new feature", "status": "open"},
        {"id": "bounty3", "title": "Write documentation", "status": "open"},
        {"id": "bounty4", "title": "Optimize database query", "status": "open"},
        {"id": "bounty5", "title": "Design UI/UX for profile page", "status": "open"},
        {"id": "bounty6", "title": "Add dark mode support", "status": "open"},
        {"id": "bounty7", "title": "Refactor old code", "status": "open"},
        {"id": "bounty8", "title": "Create a new API endpoint", "status": "open"},
        {"id": "bounty9", "title": "Debug payment gateway", "status": "open"},
    ]

def scout_bounties():
    """
    Main function to scout for new bounties, compare them against
    previously seen bounties, and alert if new ones are found.
    """
    seen_bounties_list = load_seen_bounties()
    seen_bounties_ids = {b['id'] for b in seen_bounties_list}
    
    current_bounties = fetch_current_bounties()

    new_bounties = [b for b in current_bounties if b['id'] not in seen_bounties_ids]

    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        # For simplicity, we save all current bounties as 'seen' for the next run.
        # A more robust system might merge or only add new ones.
        save_seen_bounties(current_bounties)
    else:
        print("No new bounties found.")
        # If no new bounties, ensure the seen list is up-to-date with current ones
        # (e.g., if a bounty was removed from the source)
        save_seen_bounties(current_bounties)

if __name__ == "__main__":
    # This section demonstrates how the script would run.
    # To simulate the "7 New Opportunities found" message,
    # you might need to manually prime `seen_bounties.json`
    # with fewer bounties than `fetch_current_bounties` returns.

    # Example: If `seen_bounties.json` initially contains only bounty1 and bounty2,
    # and `fetch_current_bounties` returns 9 bounties, then 7 new ones will be found.
    # For a fresh run or to reset, delete `seen_bounties.json`.

    print("Scouting for bounties...")
    scout_bounties()
    print("Scouting complete.")
    