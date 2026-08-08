
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounties that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                # Load existing bounties, ensuring it's a set for efficient lookup
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle cases where the JSON file might be empty or malformed
                print(f"Warning: {SEEN_BOUNTIES_FILE} is empty or malformed. Starting with no seen bounties.")
                return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounties to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        # Convert set to list for JSON serialization
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    """
    Simulates fetching current bounties from a source (e.g., web scraping, API).
    In a real application, this would contain the actual logic to find bounties.
    For this example, it returns a static set of bounties to simulate discovery.
    """
    # Example set of bounties. Some might be "new", some "old".
    return {
        "bounty_A_id_123", "bounty_B_id_456", "bounty_C_id_789", "bounty_D_id_101",
        "bounty_E_id_112", "bounty_F_id_131", "bounty_G_id_415", "bounty_H_id_161",
        "bounty_I_id_718", "bounty_J_id_192", "bounty_K_id_021", "bounty_L_id_223",
        "bounty_M_id_242", "bounty_N_id_526", "bounty_O_id_272"
    }

def main():
    """Main function to scout for new bounties and alert if found."""
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    # Determine which bounties are truly new
    new_bounties = current_bounties - seen_bounties
    
    new_opportunities_count = len(new_bounties)

    if new_opportunities_count > 0:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {new_opportunities_count} New Opportunities found")
        
        # Update the set of seen bounties and save it
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties detected.")

if __name__ == "__main__":
    main()
    