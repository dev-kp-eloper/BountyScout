import json
import os

def scout_bounties():
    """
    Scouts for new bounties, compares them against previously seen bounties,
    and reports any new opportunities found. It also updates the list of
    seen bounties.
    """
    # Placeholder for actual bounty fetching logic.
    # In a real scenario, this would fetch data from an external API or source.
    # For demonstration purposes, we use a static list.
    all_bounties = [
        {"id": "bounty1", "title": "Awesome new opportunity 1"},
        {"id": "bounty2", "title": "Critical fix needed"},
        {"id": "bounty3", "title": "Feature enhancement opportunity"},
        {"id": "bounty4", "title": "Another great chance"},
        {"id": "bounty5", "title": "Security vulnerability bounty"},
        {"id": "bounty6", "title": "Performance optimization task"},
        {"id": "bounty7", "title": "New UI/UX design bounty"},
    ]

    seen_bounties_file = 'seen_bounties.json'
    seen_ids = set()

    # Load previously seen bounty IDs
    if os.path.exists(seen_bounties_file):
        with open(seen_bounties_file, 'r') as f:
            try:
                # Handle empty or malformed JSON files gracefully
                content = f.read()
                if content:
                    seen_ids = set(json.loads(content))
                else:
                    print(f"Warning: {seen_bounties_file} is empty. Starting fresh.")
            except json.JSONDecodeError as e:
                print(f"Error decoding {seen_bounties_file}: {e}. Starting fresh.")
                seen_ids = set()
    else:
        print(f"Info: {seen_bounties_file} not found. A new file will be created.")

    new_bounties = []
    current_bounty_ids = set()

    # Identify new bounties and collect all current bounty IDs
    for bounty in all_bounties:
        bounty_id = bounty.get("id")
        if bounty_id:
            current_bounty_ids.add(bounty_id)
            if bounty_id not in seen_ids:
                new_bounties.append(bounty)

    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        for bounty in new_bounties:
            print(f"- {bounty.get('title', 'Untitled Bounty')} (ID: {bounty.get('id', 'N/A')})")

        # Update the seen bounties file with all current bounty IDs
        updated_seen_ids = seen_ids.union(current_bounty_ids)
        with open(seen_bounties_file, 'w') as f:
            json.dump(list(updated_seen_ids), f, indent=4)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
