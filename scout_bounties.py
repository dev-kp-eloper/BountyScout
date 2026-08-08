
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
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        # Convert set to list for JSON serialization
        json.dump(list(bounties), f, indent=4)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching all current bounties.
    In a real application, this would involve web scraping or API calls.
    Returns a set of unique bounty identifiers.
    """
    # Simulate a list of bounties that might be found in a run.
    # For demonstration, let's assume these are found.
    # The number of new bounties will depend on what's already in seen_bounties.json.
    all_bounties_found_this_run = {
        "bounty_xyz_001", "bounty_abc_002", "bounty_def_003",
        "bounty_ghi_004", "bounty_jkl_005", "bounty_mno_006",
        "bounty_pqr_007", "bounty_stu_008", "bounty_vwx_009"
    }
    return all_bounties_found_this_run

def main():
    """Main function to scout for new bounties and alert."""
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # FIX: Corrected "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        
        # Update seen bounties and save
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    