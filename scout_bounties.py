
import json
import os

# --- Placeholder for bounty fetching logic ---
def fetch_new_bounties():
    """
    Simulates fetching new bounties. In a real scenario, this would
    interact with an API or parse a webpage to find new opportunities.
    """
    # Example data:
    return [
        {"id": 101, "title": "Implement feature X"},
        {"id": 102, "title": "Fix bug Y in module Z"},
        {"id": 103, "title": "Optimize database query performance"}
    ]

def get_seen_bounties(filepath="seen_bounties.json"):
    """
    Loads the set of bounty IDs that have already been seen from a JSON file.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle case where file is empty or corrupted
            return set()
    return set()

def save_seen_bounties(bounty_ids, filepath="seen_bounties.json"):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(filepath, 'w') as f:
        json.dump(list(bounty_ids), f, indent=4)

def main():
    """
    Main function to scout for new bounties and generate an alert if found.
    """
    all_current_bounties = fetch_new_bounties()
    seen_bounty_ids = get_seen_bounties()

    new_bounties = [b for b in all_current_bounties if b["id"] not in seen_bounty_ids]

    if new_bounties:
        num_new = len(new_bounties)
        
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        issue_title = f"🎯 Bounty Alert: {num_new} New Opportunities found"
        print(issue_title)
        
        # Update seen bounties
        new_bounty_ids = {b["id"] for b in new_bounties}
        updated_seen_bounties = seen_bounty_ids.union(new_bounty_ids)
        save_seen_bounties(updated_seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    