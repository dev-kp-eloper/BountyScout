
import json
import os

# Placeholder for actual bounty scouting logic
def scout_for_bounties():
    # In a real scenario, this would fetch new bounties from various sources.
    # For demonstration, let's simulate finding 2 new bounties.
    # These bounties would ideally have unique identifiers.
    return [
        {"id": "bounty_xyz_1", "title": "Exciting Web3 Project"},
        {"id": "bounty_xyz_2", "title": "Smart Contract Audit Need"}
    ]

def main():
    seen_bounties_file = 'seen_bounties.json'
    seen_bounty_ids = set()

    # Load previously seen bounties
    if os.path.exists(seen_bounties_file):
        with open(seen_bounties_file, 'r') as f:
            try:
                data = json.load(f)
                # Ensure data is a list and contains strings (bounty IDs)
                if isinstance(data, list) and all(isinstance(item, str) for item in data):
                    seen_bounty_ids = set(data)
                else:
                    print(f"Warning: {seen_bounties_file} content is malformed. Starting fresh.")
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {seen_bounties_file}. Starting fresh.")
            except Exception as e:
                print(f"An error occurred while reading {seen_bounties_file}: {e}. Starting fresh.")
    
    new_bounties_found_count = 0
    current_bounties = scout_for_bounties()
    newly_identified_bounty_ids = set()

    for bounty in current_bounties:
        bounty_id = bounty.get("id") # Assuming bounties have a unique 'id'
        if bounty_id and bounty_id not in seen_bounty_ids:
            new_bounties_found_count += 1
            newly_identified_bounty_ids.add(bounty_id)
            print(f"New bounty found: {bounty.get('title', 'Unknown Title')} (ID: {bounty_id})")

    if new_bounties_found_count > 0:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {new_bounties_found_count} New Opportunities found")
        
        # Update seen bounties and save
        updated_seen_bounty_ids = list(seen_bounty_ids.union(newly_identified_bounty_ids))
        with open(seen_bounties_file, 'w') as f:
            json.dump(updated_seen_bounty_ids, f, indent=4)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    