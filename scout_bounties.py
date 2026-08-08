
import json
import os
import random
import time

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounties from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting fresh.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounties to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def scout_for_bounties():
    """
    Simulates the process of scouting for new bounties.
    In a real application, this would involve scraping websites or querying APIs.
    """
    current_time = int(time.time())
    bounties_found = []
    # Simulate finding a random number of bounties (e.g., between 5 and 15)
    for i in range(random.randint(5, 15)): 
        bounties_found.append(f"bounty_{current_time}_{i}")
    return set(bounties_found)

def main():
    """Main function to run the bounty scouting process."""
    print("Starting bounty scout...")
    
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()
    
    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") 
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        print(f"Successfully added {len(new_bounties)} new bounties to {SEEN_BOUNTIES_FILE}")
    else:
        print("No new bounties found.")
    
    print("Bounty scout finished.")

if __name__ == "__main__":
    main()
    