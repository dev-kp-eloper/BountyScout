
import json
import os
import time

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting with an empty seen list.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real application, this would involve API calls or web scraping.
    """
    mock_bounties = [
        {"id": "bounty_1", "title": "Fix UI bug", "value": 100},
        {"id": "bounty_2", "title": "Implement new feature", "value": 500},
        {"id": "bounty_3", "title": "Write unit tests", "value": 200},
        {"id": "bounty_4", "title": "Optimize database query", "value": 300},
        {"id": "bounty_5", "title": "Refactor legacy code", "value": 400},
        {"id": "bounty_6", "title": "Add dark mode", "value": 250},
        {"id": "bounty_7", "title": "Update dependencies", "value": 150},
        {"id": "bounty_8", "title": "Improve error handling", "value": 350},
        {"id": "bounty_9", "title": "Create CI/CD pipeline", "value": 600},
        {"id": "bounty_10", "title": "Document API endpoints", "value": 100},
        {"id": "bounty_11", "title": "Security review", "value": 700},
        {"id": "bounty_12", "title": "Performance tuning", "value": 450},
        {"id": "bounty_13", "title": "Accessibility audit", "value": 200},
        {"id": "bounty_14", "title": "Integrate payment gateway", "value": 800},
        {"id": "bounty_15", "title": "Design new logo", "value": 100},
        {"id": "bounty_16", "title": "Build mobile app", "value": 1000},
        {"id": "bounty_17", "title": "Translate content", "value": 150},
        {"id": "bounty_18", "title": "Setup analytics", "value": 250},
    ]
    # Simulate some network delay
    time.sleep(0.1)
    return mock_bounties

def scout_for_bounties():
    """
    Scouts for new bounties, identifies those not yet seen,
    reports them, and updates the seen bounties list.
    """
    print("Scouting for new bounties...")
    seen_bounties = load_seen_bounties()
    current_bounties_data = fetch_current_bounties()
    current_bounty_ids = {bounty["id"] for bounty in current_bounties_data}

    new_bounty_ids = current_bounty_ids - seen_bounties

    if new_bounty_ids:
        print(f"🎯 Bounty Alert: {len(new_bounty_ids)} New Opportunities found!")
        print("New bounties:")
        for bounty_id in new_bounty_ids:
            # Find the full bounty data for printing
            new_bounty = next((b for b in current_bounties_data if b["id"] == bounty_id), None)
            if new_bounty:
                print(f"  - {new_bounty['title']} (ID: {new_bounty['id']}, Value: ${new_bounty['value']})")
        
        # --- FIX START ---
        # Update the set of seen bounties with the newly found ones
        seen_bounties.update(new_bounty_ids)
        # Persist the updated set of seen bounties to the JSON file
        save_seen_bounties(seen_bounties)
        print(f"Successfully updated {SEEN_BOUNTIES_FILE} with {len(new_bounty_ids)} new bounties.")
        # --- FIX END ---
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_bounties()
    