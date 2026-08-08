
import json
import os

# Placeholder for actual logic to find new bounties.
# In a real scenario, this would interact with external APIs or data sources.
def get_new_bounties():
    """
    Simulates fetching new bounties.
    For this demonstration, it returns a fixed list of 7 bounties.
    """
    # In a real application, this would fetch current bounties and compare against seen_bounties.
    # We are simulating the scenario where 7 new bounties are found.
    return [
        {"id": 1, "name": "Bounty A", "description": "Solve algorithm X"},
        {"id": 2, "name": "Bounty B", "description": "Implement feature Y"},
        {"id": 3, "name": "Bounty C", "description": "Fix bug Z"},
        {"id": 4, "name": "Bounty D", "description": "Review pull request P"},
        {"id": 5, "name": "Bounty E", "description": "Write documentation for Q"},
        {"id": 6, "name": "Bounty F", "description": "Optimize query R"},
        {"id": 7, "name": "Bounty G", "description": "Design UI for S"}
    ]

def load_seen_bounties(filepath="seen_bounties.json"):
    """
    Loads the set of bounty IDs that have already been seen from a JSON file.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {filepath}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounty_ids, filepath="seen_bounties.json"):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(filepath, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def main():
    """
    Main function to scout for new bounties and alert if found.
    """
    seen_bounty_ids = load_seen_bounties()
    current_bounties = get_new_bounties() # This would typically fetch *all* current bounties

    new_bounties_found = []
    for bounty in current_bounties:
        if bounty['id'] not in seen_bounty_ids:
            new_bounties_found.append(bounty)
            seen_bounty_ids.add(bounty['id'])

    if new_bounties_found:
        # Fixed the spelling from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties_found)} New Opportunities found")
        save_seen_bounties(seen_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    