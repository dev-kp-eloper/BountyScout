
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties_ids):
    """Saves the current set of seen bounty IDs."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties_ids), f, indent=2)

def fetch_bounties_from_source():
    """
    Simulates fetching bounties from an external source.
    In a real application, this would involve API calls, web scraping, etc.
    """
    # Example mock data. In a real scenario, this would be dynamic.
    return [
        {"id": "b1", "name": "Fix Critical Bug in Auth"},
        {"id": "b2", "name": "Implement New Dashboard Feature"},
        {"id": "b3", "name": "Optimize Database Query Performance"},
        {"id": "b4", "name": "Write Comprehensive API Documentation"},
        {"id": "b5", "name": "Refactor Legacy User Module"},
        {"id": "b6", "name": "Add Unit Tests for Payment Gateway"},
        {"id": "b7", "name": "Investigate Performance Regression"},
        {"id": "b8", "name": "Update Dependencies to Latest Versions"},
    ]

def main():
    """
    Main function to scout for new bounties, alert if found, and update seen bounties.
    """
    seen_bounties_ids = load_seen_bounties()
    all_bounties = fetch_bounties_from_source()

    current_bounty_ids = {b["id"] for b in all_bounties}
    new_bounties_ids = current_bounty_ids - seen_bounties_ids

    if new_bounties_ids:
        # Fixed typo: "Opportunityies" changed to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties_ids)} New Opportunities found")
        updated_seen_bounties = seen_bounties_ids.union(current_bounty_ids)
        save_seen_bounties(updated_seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    