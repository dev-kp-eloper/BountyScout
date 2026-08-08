
import json
import os

# Placeholder for actual bounty scouting logic.
# In a real scenario, this function would interact with APIs or scrape websites.
# For the purpose of demonstrating the fix, a mock list of bounties is used.
def scout_for_bounties():
    """
    Simulates scouting for new bounties.
    Returns a list of dictionaries, each representing a bounty.
    """
    mock_bounties = [
        {"id": "b1", "title": "Fix bug in login", "value": 100},
        {"id": "b2", "title": "Implement new feature", "value": 200},
        {"id": "b3", "title": "Write documentation", "value": 50},
        {"id": "b4", "title": "Optimize database query", "value": 150},
        {"id": "b5", "title": "Add unit tests", "value": 100},
        {"id": "b6", "title": "Refactor old code", "value": 120},
        {"id": "b7", "title": "Design UI component", "value": 180},
        {"id": "b8", "title": "Security audit", "value": 250},
        {"id": "b9", "title": "Performance tuning", "value": 170},
        {"id": "b10", "title": "Accessibility improvements", "value": 130},
        {"id": "b11", "title": "Translate content", "value": 90},
        {"id": "b12", "title": "Create marketing material", "value": 110},
    ]
    return mock_bounties

def get_seen_bounties(filename="seen_bounties.json"):
    """
    Loads bounty IDs that have already been seen from a JSON file.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle empty or malformed JSON gracefully
                return set()
    return set()

def save_seen_bounties(bounty_ids, filename="seen_bounties.json"):
    """
    Saves the current set of bounty IDs to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(list(bounty_ids), f, indent=4)

def main():
    """
    Main function to scout for bounties, identify new ones, and report.
    """
    current_bounties = scout_for_bounties()
    seen_bounty_ids = get_seen_bounties()

    new_bounties = []
    current_bounty_ids = set()

    for bounty in current_bounties:
        bounty_id = bounty["id"]
        current_bounty_ids.add(bounty_id)
        if bounty_id not in seen_bounty_ids:
            new_bounties.append(bounty)

    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # CRITICAL FIX for Issue #771: Corrected typo in the alert message
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found") # <-- CHANGED 'Opportunityies' to 'Opportunities'
        # Update the list of seen bounties
        save_seen_bounties(current_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    