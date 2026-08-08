
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
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with no seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def scout_for_bounties():
    """
    Placeholder for actual bounty scouting logic.
    In a real scenario, this function would interact with external APIs,
    scrape websites, or perform other actions to discover new bounties.
    For this example, it returns a mock set of bounty IDs.
    """
    # Simulate fetching a list of current bounties
    mock_current_bounties = [
        "bounty_id_1", "bounty_id_2", "bounty_id_3", "bounty_id_4", "bounty_id_5",
        "bounty_id_6", "bounty_id_7", "bounty_id_8", "bounty_id_9", "bounty_id_10",
        "bounty_id_11", "bounty_id_12", "bounty_id_13", "bounty_id_14", "bounty_id_15"
    ]
    return set(mock_current_bounties)

def main():
    """Main function to load seen bounties, scout for new ones, and report."""
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    