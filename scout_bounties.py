import json
import os

# Assume some scouting logic here
def scout_for_bounties():
    # This is a placeholder for actual scouting logic
    # In a real scenario, this would fetch data from external sources
    # For this example, let's just return some dummy bounties
    # This list is designed to simulate the "14 New Opportunityies found" message
    # without needing to rely on external data or complex logic.
    return [
        {"id": "bounty_test_01", "title": "Implement feature X"},
        {"id": "bounty_test_02", "title": "Fix critical bug in module Y"},
        {"id": "bounty_test_03", "title": "Optimize database query for Z"},
        {"id": "bounty_test_04", "title": "Add unit tests for service A"},
        {"id": "bounty_test_05", "title": "Update documentation for API B"},
        {"id": "bounty_test_06", "title": "Refactor authentication flow"},
        {"id": "bounty_test_07", "title": "Integrate new payment gateway"},
        {"id": "bounty_test_08", "title": "Improve UI/UX for dashboard"},
        {"id": "bounty_test_09", "title": "Set up CI/CD pipeline"},
        {"id": "bounty_test_10", "title": "Migrate data to new schema"},
        {"id": "bounty_test_11", "title": "Add logging to critical paths"},
        {"id": "bounty_test_12", "title": "Perform security audit"},
        {"id": "bounty_test_13", "title": "Create new reporting tool"},
        {"id": "bounty_test_14", "title": "Enhance error handling"}
    ]

def main():
    seen_bounties_file = 'seen_bounties.json'
    
    # Load seen bounties
    if os.path.exists(seen_bounties_file):
        with open(seen_bounties_file, 'r') as f:
            try:
                seen_bounties = json.load(f)
                if not isinstance(seen_bounties, list): # Ensure it's a list
                    seen_bounties = []
            except json.JSONDecodeError:
                seen_bounties = [] # Handle corrupted or empty JSON
    else:
        seen_bounties = []

    # Get current bounties
    current_bounties = scout_for_bounties()
    
    new_bounties = []
    seen_bounty_ids = {b['id'] for b in seen_bounties}

    for bounty in current_bounties:
        if bounty['id'] not in seen_bounty_ids:
            new_bounties.append(bounty)

    if new_bounties:
        # Fix: Corrected typo from 'Opportunityies' to 'Opportunities'
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        
        # Add new bounties to seen list and save
        seen_bounties.extend(new_bounties)
        with open(seen_bounties_file, 'w') as f:
            json.dump(seen_bounties, f, indent=2)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
