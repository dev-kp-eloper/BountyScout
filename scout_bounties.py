
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads the set of bounty IDs that have already been seen from a JSON file.
    Returns an empty set if the file doesn't exist or is malformed.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with an empty set of seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """
    Saves the current set of seen bounty IDs to the specified JSON file.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_current_bounties():
    """
    Simulates fetching current bounties from a source (e.g., API, web scrape).
    In a real application, this would involve actual data retrieval.
    This placeholder implementation returns a static set of bounty IDs.
    """
    # Placeholder for actual bounty fetching logic.
    # This sample data is designed to simulate finding 7 new bounties
    # if 'bounty_id_001', 'bounty_id_002', 'bounty_id_003' were already seen.
    current_bounty_ids = {
        "bounty_id_001", "bounty_id_002", "bounty_id_003",
        "bounty_id_004", "bounty_id_005", "bounty_id_006",
        "bounty_id_007", "bounty_id_008", "bounty_id_009", "bounty_id_010"
    }
    return current_bounty_ids

def main():
    """
    Main function to scout for new bounties, alert if found, and update the
    list of seen bounties.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    