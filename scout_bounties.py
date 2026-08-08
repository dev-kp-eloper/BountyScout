
import json
import os
import datetime

# Configuration for the file storing seen bounties
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties_set):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        # Convert set to list for JSON serialization
        json.dump(sorted(list(bounties_set)), f, indent=2)

def fetch_current_bounties():
    """
    Simulates fetching current bounties from a source (e.g., API, web scrape).
    In a real scenario, this would contain logic to retrieve actual bounties.
    For this example, it returns a mock set of bounty IDs.
    """
    # Mock data: Let's assume some bounties are always present,
    # and some "new" ones appear based on a simple condition for demonstration.
    base_bounties = {f"bounty_id_{i:03d}" for i in range(1, 10)}
    
    # Simulate finding new bounties, sometimes 7 to match the issue title
    if datetime.datetime.now().minute % 2 == 0: # Simple condition for demonstration
        newly_discovered = {f"new_bounty_{i:02d}" for i in range(1, 8)} # 7 new ones
        return base_bounties.union(newly_discovered)
    else:
        return base_bounties.union({f"another_new_{i:02d}" for i in range(1, 3)}) # Fewer new ones

def main():
    """
    Main function to scout for new bounties, report them, and update the
    list of seen bounties.
    """
    print("Scouting for new bounties...")
    
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        
        print(f"Successfully updated {SEEN_BOUNTIES_FILE} with {len(new_bounties)} new bounties.")
        # Optional: Print details of the new bounties
        # for bounty_id in sorted(list(new_bounties)):
        #     print(f"  - {bounty_id}")
    else:
        print("No new bounties found this run.")
        print(f"Total bounties seen: {len(seen_bounties)}")

if __name__ == "__main__":
    main()
    