
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads bounty IDs that have been previously seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle empty or malformed JSON gracefully
                return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def find_new_bounties():
    """
    Simulates finding new bounties. In a real scenario, this would involve
    scraping a source for bounties and comparing them against seen ones.
    """
    # Simulate a list of all currently available bounties
    # In a real application, this would come from a web scraper or API
    all_current_bounties = {
        "bounty_id_1", "bounty_id_2", "bounty_id_3",
        "bounty_id_4", "bounty_id_5", "bounty_id_6",
        "bounty_id_7", "bounty_id_8", "bounty_id_9",
        "bounty_id_10"
    }

    seen_bounties = load_seen_bounties()
    
    # Determine which bounties are new
    new_bounties = all_current_bounties - seen_bounties

    # Update the set of seen bounties with all current bounties
    # This ensures that next run, these won't be considered "new"
    seen_bounties.update(all_current_bounties)
    save_seen_bounties(seen_bounties)

    return list(new_bounties)

if __name__ == "__main__":
    new_opportunities = find_new_bounties()
    num_new = len(new_opportunities)

    if num_new > 0:
        # FIX: Corrected "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
        for bounty_id in new_opportunities:
            print(f"- {bounty_id}")
    else:
        print("No new bounties found.")
    print(f"Total bounties seen: {len(load_seen_bounties())}")
