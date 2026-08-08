
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounty IDs from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting fresh.")
                return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def scout_for_bounties():
    """
    Placeholder function to simulate scouting for new bounties.
    In a real application, this would involve API calls or web scraping.
    """
    print("Scouting for bounties...")
    # Simulate finding some bounties.
    # For demonstration, let's say these are found on a given run.
    all_found_bounties = {
        "bounty_id_101", "bounty_id_102", "bounty_id_103",
        "bounty_id_104", "bounty_id_105", "bounty_id_106",
        "bounty_id_107", "bounty_id_108", "bounty_id_109",
        "bounty_id_110"
    }
    # To simulate new bounties being found over runs,
    # you might add more IDs here or fetch from a dynamic source.
    return all_found_bounties

def main():
    """Main function to load seen bounties, scout for new ones, and alert."""
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        num_new = len(new_bounties)
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    