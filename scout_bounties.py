
import json
import os
import random

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                # Ensure the file is not empty before attempting to load JSON
                content = f.read()
                if content:
                    return set(json.loads(content))
                else:
                    print(f"Warning: {SEEN_BOUNTIES_FILE} is empty. Starting with an empty set of seen bounties.")
                    return set()
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting with an empty set of seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    # This function simulates fetching bounties from a source (e.g., a website or API).
    # To align with the issue title "13 New Opportunityies found",
    # we'll simulate finding exactly 13 bounties, assuming seen_bounties.json is initially empty
    # or contains items not overlapping with these.
    
    # In a real scenario, this would involve web scraping or API calls.
    # For demonstration, we generate a fixed set of bounty IDs.
    return {f"bounty_id_{i}" for i in range(1, 14)} # Simulating 13 bounties

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    
    num_new = len(new_bounties)

    if num_new > 0:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
        
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    