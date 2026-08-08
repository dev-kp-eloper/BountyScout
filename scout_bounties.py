
import json
import os

# Placeholder function for fetching bounties from an external source
def fetch_all_bounties():
    """
    Simulates fetching current bounties. In a real application, this would
    interface with an external API or data source.
    """
    # Example data; assume these are new until marked seen
    return [
        {"id": "bounty_001", "title": "Help wanted for project Alpha"},
        {"id": "bounty_002", "title": "Translate documentation to Spanish"},
        {"id": "bounty_003", "title": "Bug fix: UI alignment issue"},
        {"id": "bounty_004", "title": "Feature request: Dark mode implementation"},
        {"id": "bounty_005", "title": "Write unit tests for authentication module"},
        {"id": "bounty_006", "title": "Optimize database queries"},
        {"id": "bounty_007", "title": "Design a new logo"},
        {"id": "bounty_008", "title": "Create a tutorial video"},
        {"id": "bounty_009", "title": "Refactor legacy code in module X"},
        {"id": "bounty_010", "title": "Research new API integration methods"},
        {"id": "bounty_011", "title": "Update dependencies to latest versions"},
        {"id": "bounty_012", "title": "Implement multi-factor authentication"},
    ]

def load_seen_bounties(filepath="seen_bounties.json"):
    """Loads a set of bounty IDs that have already been processed."""
    if not os.path.exists(filepath):
        return set()
    try:
        with open(filepath, 'r') as f:
            return set(json.load(f))
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading seen bounties: {e}")
        return set()

def save_seen_bounties(seen_ids, filepath="seen_bounties.json"):
    """Saves the current set of seen bounty IDs."""
    try:
        with open(filepath, 'w') as f:
            json.dump(list(seen_ids), f, indent=4)
    except IOError as e:
        print(f"Error saving seen bounties: {e}")

def main():
    """
    Main function to scout for new bounties, report them, and update
    the list of seen bounties.
    """
    print("Scouting for new bounties...")
    seen_bounty_ids = load_seen_bounties()
    current_bounties = fetch_all_bounties()

    new_bounties = []
    for bounty in current_bounties:
        if bounty["id"] not in seen_bounty_ids:
            new_bounties.append(bounty)
            seen_bounty_ids.add(bounty["id"])

    if new_bounties:
        count = len(new_bounties)
        # FIX: Corrected "Opportunityies" to "Opportunities"
        issue_title = f"🎯 Bounty Alert: {count} New Opportunities found"
        print(issue_title)
        print("New bounties:")
        for bounty in new_bounties:
            print(f"- {bounty['title']} (ID: {bounty['id']})")
        save_seen_bounties(seen_bounty_ids)
        print(f"Updated seen_bounties.json with {count} new bounties.")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    