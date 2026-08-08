
import json
import os

# Define the path for the seen bounties file
SEEN_BOUNTIES_FILE = "seen_bounties.json"

def load_seen_bounties():
    """Loads a set of seen bounty IDs from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle empty or malformed JSON file
                return set()
    return set()

def save_seen_bounties(bounty_ids):
    """Saves a set of bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real scenario, this would involve API calls, scraping, etc.
    """
    # Simulate some new bounties being found for demonstration
    # This list would typically come from an external source
    return [
        {"id": "bounty_101", "title": "Implement Feature X", "url": "http://example.com/b101"},
        {"id": "bounty_102", "title": "Fix Bug Y", "url": "http://example.com/b102"},
        {"id": "bounty_103", "title": "Optimize Z", "url": "http://example.com/b103"},
        {"id": "bounty_104", "title": "Write Docs", "url": "http://example.com/b104"},
        {"id": "bounty_105", "title": "Refactor Code", "url": "http://example.com/b105"},
        {"id": "bounty_106", "title": "Review PR", "url": "http://example.com/b106"},
    ]

def main():
    """Main function to scout for new bounties and alert."""
    print("Scouting for new bounties...")

    current_bounties = fetch_current_bounties()
    current_bounty_ids = {b['id'] for b in current_bounties}

    seen_bounty_ids = load_seen_bounties()

    new_bounty_ids = current_bounty_ids - seen_bounty_ids
    new_bounties = [b for b in current_bounties if b['id'] in new_bounty_ids]

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        for bounty in new_bounties:
            print(f"- {bounty['title']} ({bounty['url']})")
        
        # Update seen bounties and save
        seen_bounty_ids.update(new_bounty_ids)
        save_seen_bounties(seen_bounty_ids)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {len(new_bounties)} new bounties.")
    else:
        print("No new bounties found this run.")

if __name__ == "__main__":
    main()
    