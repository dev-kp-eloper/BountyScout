
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads a set of seen bounty IDs from the seen_bounties.json file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle case where file is empty or malformed
            print(f"Warning: {SEEN_BOUNTIES_FILE} is empty or corrupted. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to the seen_bounties.json file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def find_current_bounties():
    """
    Placeholder for actual bounty scraping/API calls.
    In a real scenario, this would fetch data from external sources.
    For demonstration, returning some mock bounties.
    """
    # Simulate fetching bounties from an external source
    # These bounties include some that might be new on a fresh run,
    # and some that might already be "seen" after the first run.
    return [
        {'id': 'bounty_1', 'title': 'Fix login bug'},
        {'id': 'bounty_2', 'title': 'Add new feature X'},
        {'id': 'bounty_3', 'title': 'Optimize database query'},
        {'id': 'bounty_4', 'title': 'Write unit tests'},
        {'id': 'bounty_5', 'title': 'Implement user profile page'},
        {'id': 'bounty_6', 'title': 'Improve search algorithm'},
        {'id': 'bounty_7', 'title': 'Refactor authentication module'},
        {'id': 'bounty_8', 'title': 'Update dependencies'},
    ]

def main():
    """
    Main function to scout for new bounties, update the seen list,
    and report new opportunities.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = find_current_bounties()

    updated_seen_bounties = set(seen_bounties)
    new_bounties_count = 0  # Initialize counter for new bounties

    for bounty in current_bounties:
        bounty_id = bounty['id'] # Assuming 'id' is a unique identifier for a bounty
        if bounty_id not in updated_seen_bounties:
            updated_seen_bounties.add(bounty_id)
            new_bounties_count += 1  # Increment counter if a new bounty is found
    
    save_seen_bounties(updated_seen_bounties)

    # Report the number of new opportunities found
    if new_bounties_count > 0:
        print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunities found")
    else:
        print("No new bounties found.")

if __name__ == '__main__':
    main()
    