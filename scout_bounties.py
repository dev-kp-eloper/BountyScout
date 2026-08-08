
import json
import os
import time

def load_seen_bounties(filepath="seen_bounties.json"):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_bounties(seen_ids, filepath="seen_bounties.json"):
    with open(filepath, 'w') as f:
        json.dump(list(seen_ids), f, indent=4)

def fetch_new_bounties():
    # Simulate fetching new bounties
    # In a real scenario, this would involve web scraping or API calls
    all_possible_bounties = [
        {"id": "b1", "title": "Fix a bug"},
        {"id": "b2", "title": "Add a feature"},
        {"id": "b3", "title": "Write documentation"},
        {"id": "b4", "title": "Optimize performance"},
        {"id": "b5", "title": "Security review"},
        {"id": "b6", "title": "UI/UX improvements"},
        {"id": "b7", "title": "Database migration"},
        {"id": "b8", "title": "API integration"},
        {"id": "b9", "title": "Testing framework setup"},
        {"id": "b10", "title": "Refactor old code"},
        {"id": "b11", "title": "New opportunity 1"},
        {"id": "b12", "title": "New opportunity 2"},
        {"id": "b13", "title": "New opportunity 3"},
        {"id": "b14", "title": "New opportunity 4"},
        {"id": "b15", "title": "New opportunity 5"},
        {"id": "b16", "title": "New opportunity 6"},
        {"id": "b17", "title": "New opportunity 7"},
        {"id": "b18", "title": "New opportunity 8"},
        {"id": "b19", "title": "New opportunity 9"},
        {"id": "b20", "title": "New opportunity 10"},
    ]
    # For simulation, let's say 10 new ones are found each time
    # A more realistic scenario would fetch fresh data and compare
    return all_possible_bounties[10:20] # Return 10 "new" bounties for example

def scout_for_bounties():
    seen_ids = load_seen_bounties()
    new_bounties = []
    
    fetched_bounties = fetch_new_bounties()
    
    for bounty in fetched_bounties:
        if bounty['id'] not in seen_ids:
            new_bounties.append(bounty)
            seen_ids.add(bounty['id'])
            
    if new_bounties:
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") # THIS LINE WAS MODIFIED
        for bounty in new_bounties:
            print(f"- {bounty['title']} (ID: {bounty['id']})")
        save_seen_bounties(seen_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    print("Scouting for bounties...")
    scout_for_bounties()
    print("Scouting complete.")
    