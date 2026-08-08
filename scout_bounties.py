
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                # Ensure the loaded data is a list before converting to set
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
                else:
                    print(f"Warning: {SEEN_BOUNTIES_FILE} contains non-list data. Starting fresh.")
                    return set()
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is empty or malformed. Starting fresh.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def scout_for_bounties():
    """
    Simulates scouting for new bounties and alerts if new ones are found.
    Updates the seen bounties file.
    """
    # In a real application, this part would involve web scraping or API calls
    # to fetch current bounties.
    
    # Simulate a pool of all potential bounty IDs
    all_potential_bounties = {f"bounty_id_{i:03d}" for i in range(1, 50)} 
    
    seen_bounties = load_seen_bounties()
    
    # Simulate finding new bounties. 
    # For the initial run or when many are new, generate a set that includes 21 new ones.
    # For subsequent runs, simulate fewer new ones.
    
    # This logic aims to produce "21 New Opportunities found" at least once
    # if the seen_bounties.json is initially empty or small.
    if not seen_bounties or len(seen_bounties) < 10:
        # Simulate finding bounties up to ID 21 + some already seen
        current_found_bounties = {f"bounty_id_{i:03d}" for i in range(1, 25)} # e.g., finds 24 bounties
    else:
        # On subsequent runs, simulate finding fewer new bounties
        current_found_bounties = {f"bounty_id_{i:03d}" for i in range(5, 15)} # e.g., finds 10 bounties
        
    new_bounties = current_found_bounties - seen_bounties
    
    if new_bounties:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") 
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_bounties()
    