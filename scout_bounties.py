
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

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_bounties_from_source():
    """
    Placeholder for actual bounty scraping logic.
    In a real application, this would fetch bounties from external sources.
    Returns a set of unique bounty identifiers.
    """
    # Simulate fetching some bounties, including some new ones
    # This mock data is set up to potentially trigger an alert with multiple new bounties
    all_bounties = {
        "bounty_A_1", "bounty_B_2", "bounty_C_3", "bounty_D_4", "bounty_E_5",
        "bounty_F_6", "bounty_G_7", "bounty_H_8", "bounty_I_9", "bounty_J_10",
        "bounty_K_11", "bounty_L_12", "bounty_M_13", "bounty_N_14", "bounty_O_15"
    }
    return all_bounties

def main():
    """Main function to scout for new bounties and alert."""
    print("Scouting for new bounties...")
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_bounties_from_source()

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        count = len(new_bounties)
        # Construct the alert message
        if count == 1:
            alert_message = f"🎯 Bounty Alert: {count} New Opportunity found"
        else:
            # FIX: Corrected typo from "Opportunityies" to "Opportunities"
            alert_message = f"🎯 Bounty Alert: {count} New Opportunities found" # ISSUE #726 FIX
        
        print(alert_message)
        
        # Update seen bounties and save
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
        print(f"Updated {len(new_bounties)} new bounties to seen_bounties.json.")
    else:
        print("No new bounties found. All bounties have been seen.")

if __name__ == "__main__":
    main()
    