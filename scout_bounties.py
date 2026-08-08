
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_bounties(seen_bounties):
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    # This function would contain logic to scrape or fetch current bounties.
    # For demonstration purposes, returning a dummy set of bounty IDs.
    return {
        "bounty_id_1", "bounty_id_2", "bounty_id_3",
        "bounty_id_4", "bounty_id_5", "bounty_id_6",
        "bounty_id_7", "bounty_id_8", "bounty_id_9",
        "bounty_id_10", "bounty_id_11", "bounty_id_12",
        "bounty_id_13", "bounty_id_14" # Added a couple more for variability
    }

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL CHANGE: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    