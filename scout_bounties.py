
import json
import time

def scout_for_bounties():
    # Simulate finding new bounties (replace with actual bounty scouting logic)
    new_bounties = [
        {"id": 1, "title": "Fix login bug", "reward": 100},
        {"id": 2, "title": "Implement new feature", "reward": 200},
        {"id": 3, "title": "Write unit tests", "reward": 50},
        {"id": 4, "title": "Update documentation", "reward": 30},
        {"id": 5, "title": "Optimize database query", "reward": 150},
    ]

    try:
        with open('seen_bounties.json', 'r') as f:
            seen_bounties = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        seen_bounties = set()

    found_new_count = 0
    current_bounty_ids = set()
    for bounty in new_bounties:
        current_bounty_ids.add(bounty["id"])
        if bounty["id"] not in seen_bounties:
            print(f"New bounty found: {bounty['title']} (ID: {bounty['id']})")
            found_new_count += 1

    if found_new_count > 0:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {found_new_count} New Opportunities found") 
    else:
        print("No new bounties found this round.")

    # Update seen bounties
    with open('seen_bounties.json', 'w') as f:
        json.dump(list(current_bounty_ids), f)

if __name__ == "__main__":
    print("Scouting for bounties...")
    scout_for_bounties()
    print("Scouting complete.")
    