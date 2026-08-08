
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle case where file is empty or malformed
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed or empty. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def scout_for_bounties():
    """
    Placeholder function to simulate scouting for new bounties.
    In a real application, this would involve API calls, web scraping, etc.
    It should return a set of unique identifiers for all currently found bounties.
    """
    # Simulate finding some bounties.
    # For demonstration, let's assume these are found in the current run.
    # In a real scenario, this would fetch actual bounty data.
    mock_bounties = {
        "bounty_id_alpha",
        "bounty_id_beta",
        "bounty_id_gamma",
        "bounty_id_delta",
        "bounty_id_epsilon",
        "bounty_id_zeta"
    }
    return mock_bounties

def main():
    """Main function to scout for new bounties and alert if found."""
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        count = len(new_bounties)
        # FIX: Corrected the typo from "Opportunityies" to "Opportunities"
        print(f"Bounty Alert: {count} New Opportunities found")
        
        # Update seen bounties with the newly found ones
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
