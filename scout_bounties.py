
# scout_bounties.py

import json
import random

# This script is assumed to scout for new bounties and report them.
# The following functions are placeholders to simulate the original functionality
# that would lead to the issue's alert message.

def get_latest_bounties():
    """
    Simulates fetching bounties from an external source.
    In a real scenario, this would involve API calls or web scraping.
    """
    # Placeholder for actual bounty fetching logic
    return [f"bounty_{i}" for i in range(random.randint(50, 100))]

def load_seen_bounties():
    """
    Loads previously seen bounties from seen_bounties.json.
    """
    try:
        with open('seen_bounties.json', 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen_bounties(bounties_set):
    """
    Saves the current set of seen bounties to seen_bounties.json.
    """
    with open('seen_bounties.json', 'w') as f:
        json.dump(list(bounties_set), f, indent=4)

def scout_for_new_bounties():
    """
    Compares latest bounties with seen bounties to find new ones.
    """
    latest_bounties = set(get_latest_bounties())
    seen_bounties = load_seen_bounties()

    new_bounties = latest_bounties - seen_bounties
    
    # Update seen bounties with the latest fetched ones
    updated_seen_bounties = seen_bounties.union(latest_bounties)
    save_seen_bounties(updated_seen_bounties)

    return len(new_bounties)

def main():
    new_opportunities_count = scout_for_new_bounties()
    
    if new_opportunities_count > 0:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {new_opportunities_count} New Opportunities found")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    