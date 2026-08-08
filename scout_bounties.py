
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have been seen before."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            # Ensure the loaded data is a list before converting to set
            return set(json.load(f))
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def scout_for_new_bounties():
    """
    Simulates scouting for new bounties.
    In a real application, this would fetch data from external sources.
    """
    # Placeholder for actual scouting logic.
    # For demonstration, let's return a fixed set of "found" bounties.
    # This set will include some "new" ones compared to an empty seen_bounties.json
    all_found_bounties = {
        "bounty_id_alpha", "bounty_id_beta", "bounty_id_gamma",
        "bounty_id_delta", "bounty_id_epsilon", "bounty_id_zeta",
        "bounty_id_eta", "bounty_id_theta", "bounty_id_iota",
        "bounty_id_kappa", "bounty_id_lambda", "bounty_id_mu",
        "existing_bounty_1", "existing_bounty_2"
    }
    return all_found_bounties

def main():
    """Main function to scout for bounties and report new ones."""
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_new_bounties()

    new_bounties = current_bounties - seen_bounties
    new_bounties_count = len(new_bounties)

    if new_bounties_count > 0:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunities found")
        # Update seen bounties with the newly found ones
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
