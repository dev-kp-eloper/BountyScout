
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounty IDs from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting fresh.")
            return set()
    return set()

def save_seen_bounties(bounty_ids):
    """Saves the current set of bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def fetch_new_bounties():
    """
    Placeholder function to simulate fetching new bounties.
    In a real scenario, this would involve scraping a website or querying an API.
    """
    # For demonstration, returns a fixed list of dummy bounties.
    return [
        {"id": "bounty_101", "title": "Fix a bug in frontend"},
        {"id": "bounty_102", "title": "Add new feature X"},
        {"id": "bounty_103", "title": "Optimize database query"},
        {"id": "bounty_104", "title": "Write unit tests"},
        {"id": "bounty_105", "title": "Documentation update"},
        {"id": "bounty_106", "title": "Refactor old code"},
        {"id": "bounty_107", "title": "Implement caching"},
        {"id": "bounty_108", "title": "Design a new UI component"},
        {"id": "bounty_109", "title": "Security audit"},
        {"id": "bounty_110", "title": "Performance tuning"},
    ]

def scout_bounties():
    """
    Main function to scout for new bounties, identify unseen ones,
    update the seen bounties list, and report new opportunities.
    """
    seen_bounty_ids = load_seen_bounties()
    
    all_found_bounties = fetch_new_bounties()
    
    new_bounties = []
    current_bounty_ids = set()
    
    for bounty in all_found_bounties:
        bounty_id = bounty['id']
        current_bounty_ids.add(bounty_id)
        if bounty_id not in seen_bounty_ids:
            new_bounties.append(bounty)
            
    # Update the seen bounties file with all bounties encountered in this run
    # This ensures that even if some bounties are no longer fetched,
    # the existing ones are still marked as seen.
    save_seen_bounties(seen_bounty_ids.union(current_bounty_ids))
    
    new_bounties_count = len(new_bounties)
    
    if new_bounties_count > 0:
        # Fixed typo: "Opportunityies" changed to "Opportunities"
        print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunities found")
        for bounty in new_bounties:
            print(f"- ID: {bounty['id']}, Title: {bounty['title']}")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
