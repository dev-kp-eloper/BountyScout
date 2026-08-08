
import json
import time
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_bounties(seen_bounties):
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f)

def find_new_bounties():
    # This is a placeholder for actual bounty scouting logic
    # In a real scenario, this would scrape websites, APIs, etc.
    all_bounties = {
        "bounty_id_1": {"title": "Fix a CSS bug", "url": "http://example.com/b1"},
        "bounty_id_2": {"title": "Implement new feature", "url": "http://example.com/b2"},
        "bounty_id_3": {"title": "Write unit tests", "url": "http://example.com/b3"},
        "bounty_id_4": {"title": "Documentation update", "url": "http://example.com/b4"},
        "bounty_id_5": {"title": "Refactor old code", "url": "http://example.com/b5"}
    }
    return all_bounties

def scout_bounties():
    seen_bounties = load_seen_bounties()
    all_bounties = find_new_bounties()
    new_bounties = []

    for bounty_id, bounty_info in all_bounties.items():
        if bounty_id not in seen_bounties:
            new_bounties.append(bounty_info)
            seen_bounties.add(bounty_id)

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") 
        for bounty in new_bounties:
            print(f"- {bounty['title']} ({bounty['url']})")
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    print("Scouting for bounties...")
    scout_bounties()
    print("Scouting complete.")
    