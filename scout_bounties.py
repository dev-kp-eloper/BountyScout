
import json
import os

def load_seen_bounties(filename="seen_bounties.json"):
    """
    Loads the set of bounties that have already been seen from a JSON file.
    """
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle cases where the JSON file might be empty or malformed
            return set()
    return set()

def save_seen_bounties(bounties, filename="seen_bounties.json"):
    """
    Saves the current set of seen bounties to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def scout_for_bounties():
    """
    Simulates scouting for new bounties, compares them against seen bounties,
    and reports new opportunities.
    """
    # This section would contain the actual logic to 'scout' for bounties,
    # e.g., via web scraping or API calls to various bounty platforms.
    # For this example, we simulate a list of currently available bounties.
    
    # Simulate a list of currently available bounties.
    # On a first run, 8 of these would be considered "new" if seen_bounties.json is empty.
    current_bounties = {
        "bounty_id_123", 
        "bounty_id_456", 
        "bounty_id_789",
        "bounty_id_101",
        "bounty_id_112",
        "bounty_id_131",
        "bounty_id_415",
        "bounty_id_617", 
        "existing_bounty_1", 
        "existing_bounty_2"
    }

    seen_bounties = load_seen_bounties()
    
    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        # Update the seen bounties with the newly found ones
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"Bounty Alert: {len(new_bounties)} New Opportunities found")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_bounties()
