
import json
import os

# This script is designed to scout for new bounties,
# compare them against previously seen bounties, and
# alert when new opportunities are found.

def load_seen_bounties(filepath="seen_bounties.json"):
    """
    Loads the set of bounty IDs that have been seen previously.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {filepath}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties, filepath="seen_bounties.json"):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(filepath, 'w') as f:
        json.dump(list(bounties), f, indent=4)

def fetch_current_bounties():
    """
    Simulates fetching current bounties from a source.
    In a real application, this would involve API calls, web scraping, etc.
    For demonstration, it returns a hardcoded set of bounty IDs.
    """
    # Example mock data, simulating 12 active bounties
    # This list can change over time to simulate new bounties appearing.
    return {
        "bounty_xyz_001", "bounty_xyz_002", "bounty_xyz_003",
        "bounty_xyz_004", "bounty_xyz_005", "bounty_xyz_006",
        "bounty_xyz_007", "bounty_xyz_008", "bounty_xyz_009",
        "bounty_xyz_010", "bounty_xyz_011", "bounty_xyz_012",
        # Add more bounties here to simulate new opportunities over runs
        # e.g., "bounty_xyz_013", "bounty_xyz_014"
    }

def scout_bounties():
    """
    Main function to scout for new bounties and report them.
    """
    print("Scouting for new bounties...")
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    num_new = len(new_bounties)

    if num_new > 0:
        # FIX: Corrected typo from 'Opportunityies' to 'Opportunities'
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
        for bounty_id in new_bounties:
            print(f"  - New Bounty ID: {bounty_id}")
        
        # Update seen bounties to include the newly found ones
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        print(f"Updated seen_bounties.json with {num_new} new bounties.")
    else:
        print("No new bounties found this run.")

if __name__ == "__main__":
    scout_bounties()
    