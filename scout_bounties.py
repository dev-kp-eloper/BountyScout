
import json
import os

# Placeholder for actual bounty fetching logic
def fetch_current_bounties():
    # In a real scenario, this would scrape websites or call APIs
    # For this example, let's return some dummy data that would result in new bounties
    # to simulate the alert message from the issue.
    # The actual content of this function would be preserved if the original file was available.
    return [
        {"id": "bounty1", "title": "Fix a bug in backend", "source": "platformX"},
        {"id": "bounty2", "title": "Develop new UI component", "source": "platformY"},
        {"id": "bounty3", "title": "Write documentation", "source": "platformX"},
        {"id": "bounty4", "title": "Security audit", "source": "platformZ"},
        {"id": "bounty5", "title": "Performance optimization", "source": "platformX"},
        {"id": "bounty6", "title": "Data migration", "source": "platformY"},
        {"id": "bounty7", "title": "API integration", "source": "platformZ"},
        {"id": "bounty8", "title": "Mobile app development", "source": "platformX"},
        {"id": "bounty9", "title": "Database design", "source": "platformY"}, # This would be new if 8 were seen
        {"id": "bounty10", "title": "Cloud infrastructure setup", "source": "platformZ"}, # This would be new
    ]

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounty IDs from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
                return set()
    return set()

def save_seen_bounties(bounty_ids):
    """Saves the current set of bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def main():
    print("Scouting for new bounties...")
    current_bounties = fetch_current_bounties()
    seen_bounty_ids = load_seen_bounties()

    new_bounties = []
    current_bounty_ids = set()

    for bounty in current_bounties:
        bounty_id = bounty['id']
        current_bounty_ids.add(bounty_id)
        if bounty_id not in seen_bounty_ids:
            new_bounties.append(bounty)

    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        for bounty in new_bounties:
            print(f"- {bounty['title']} ({bounty['source']})")
    else:
        print("No new bounties found.")

    # Update seen bounties with the current set
    save_seen_bounties(current_bounty_ids)

if __name__ == "__main__":
    main()
    