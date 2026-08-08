
import json
import os
import random # For simulating new bounties

SEEN_BOUNTIES_FILE = "seen_bounties.json"

def load_seen_bounties():
    """
    Loads the set of bounty IDs that have been seen previously from a JSON file.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                # Load as list and convert to set for efficient lookup
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle cases where the file might be empty or malformed JSON
                print(f"Warning: {SEEN_BOUNTIES_FILE} is empty or malformed. Starting with no seen bounties.")
                return set()
    return set()

def save_seen_bounties(bounties_set):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        # Convert set to list for JSON serialization
        json.dump(list(bounties_set), f, indent=4)

def fetch_current_bounties():
    """
    Simulates fetching current bounties from various sources.
    In a real-world application, this function would contain logic
    to scrape websites, query APIs, etc., to get the latest bounties.
    For this example, it generates a random set of bounty IDs.
    """
    num_bounties = random.randint(5, 15) # Simulate a varying number of bounties
    current_bounties = {f"bounty_{i:03d}" for i in range(num_bounties)}
    # Add a few consistent bounties to ensure some are always 'seen'
    current_bounties.add("bounty_static_001")
    current_bounties.add("bounty_static_002")
    return current_bounties

def main():
    """
    Main function to scout for new bounties, alert on new opportunities,
    and update the list of seen bounties.
    """
    print("Scouting for new bounties...")
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties) # Add new bounties to the seen set
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found this run.")
    
    print(f"Total unique bounties seen so far: {len(seen_bounties)}")

if __name__ == "__main__":
    main()
    