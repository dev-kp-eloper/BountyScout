
import json
import os
import time

# Placeholder for actual bounty fetching logic
def fetch_current_bounties():
    """
    Simulates fetching a list of current bounties.
    This content is designed to produce "6 New Opportunities found"
    if 'seen_bounties.json' is empty or does not contain these IDs.
    """
    return [
        {"id": "b1", "title": "Fix login bug", "url": "http://example.com/b1"},
        {"id": "b2", "title": "Implement new feature", "url": "http://example.com/b2"},
        {"id": "b3", "title": "Write unit tests", "url": "http://example.com/b3"},
        {"id": "b4", "title": "Optimize database query", "url": "http://example.com/b4"},
        {"id": "b5", "title": "Update documentation", "url": "http://example.com/b5"},
        {"id": "b6", "title": "Refactor old code", "url": "http://example.com/b6"},
    ]

def load_seen_bounties(filepath="seen_bounties.json"):
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {filepath} is corrupted or empty. Starting fresh.")
            return set()
    return set()

def save_seen_bounties(seen_bounties, filepath="seen_bounties.json"):
    """Saves the set of seen bounty IDs to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def scout_bounties():
    """
    Scouts for new bounties, identifies unseen ones,
    prints an alert, and updates the seen bounties list.
    """
    print("Scouting for new bounties...")
    current_bounties = fetch_current_bounties()
    seen_bounty_ids = load_seen_bounties()

    new_bounties = []
    for bounty in current_bounties:
        if bounty["id"] not in seen_bounty_ids:
            new_bounties.append(bounty)
            seen_bounty_ids.add(bounty["id"])

    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        for bounty in new_bounties:
            print(f"- {bounty['title']} ({bounty['url']})")
        save_seen_bounties(seen_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    