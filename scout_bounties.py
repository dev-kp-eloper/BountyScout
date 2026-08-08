
import json
import time

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounty IDs from a JSON file."""
    try:
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty/corrupt, start with an empty set.
        return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f)

def fetch_new_bounties():
    """
    Placeholder function to simulate fetching all currently available bounties.
    In a real scenario, this would involve web scraping or API calls.
    """
    # Simulate a list of current bounties, some of which might be new.
    all_bounties = {
        "bounty_id_1", "bounty_id_2", "bounty_id_3",
        "bounty_id_4", "bounty_id_5", "bounty_id_6",
        "bounty_id_7", "bounty_id_8", "bounty_id_9",
        "bounty_id_10", "bounty_id_11", "bounty_id_12"
    }
    # Add a unique ID each time to simulate new bounties over runs
    all_bounties.add(f"dynamic_bounty_{int(time.time())}")
    return all_bounties

def main():
    """Main function to scout for new bounties and report them."""
    print("Starting bounty scout...")
    
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_new_bounties()

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found") 
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

    print("Bounty scout finished.")

if __name__ == "__main__":
    main()
    