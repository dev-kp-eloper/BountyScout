
# scout_bounties.py
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
        json.dump(list(seen_bounties), f)

def find_new_bounties():
    # This function would contain the logic to scrape/find bounties.
    # For demonstration, let's assume it returns a list of bounty IDs.
    # We'll simulate finding 8 new ones for the issue context.
    all_current_bounties = {"bounty_a", "bounty_b", "bounty_c", "bounty_d",
                            "bounty_e", "bounty_f", "bounty_g", "bounty_h",
                            "existing_bounty_1", "existing_bounty_2"}

    seen = load_seen_bounties()
    new_bounties = all_current_bounties - seen
    return list(new_bounties)

def main():
    new_opportunities = find_new_bounties()
    if new_opportunities:
        # Fix: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        # Update seen bounties (assuming this happens after alerting)
        seen = load_seen_bounties()
        seen.update(new_opportunities)
        save_seen_bounties(seen)
    else:
        print("No new bounties found this run.")

if __name__ == "__main__":
    main()
    