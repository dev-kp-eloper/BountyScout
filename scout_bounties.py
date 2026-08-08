
import json
import os
import time # For simulating fetching, if needed, but let's keep it simple

# --- Existing functions (hypothetical, but common for such scripts) ---
def fetch_current_bounties():
    """
    Simulates fetching current bounties from a source.
    In a real scenario, this would hit an API or scrape a website.
    Returns a list of dictionaries, each representing a bounty.
    Assume bounties have at least an 'id' field.
    """
    # For demonstration purposes, let's return some dummy bounties.
    # In a real run, these would be dynamically fetched.
    # The example bounties are crafted to show a scenario where if not persisted,
    # 'b4' and 'b5' (and potentially more if the actual list is larger)
    # would be repeatedly identified as 'new'.
    return [
        {"id": "b1", "title": "Fix login bug", "reward": 100},
        {"id": "b2", "title": "Implement new feature X", "reward": 250},
        {"id": "b3", "title": "Optimize database query", "reward": 150},
        {"id": "b4", "title": "Add testing framework", "reward": 300},
        {"id": "b5", "title": "Update documentation", "reward": 50},
        {"id": "b6", "title": "Refactor API endpoints", "reward": 400},
        {"id": "b7", "title": "Improve error logging", "reward": 120},
        {"id": "b8", "title": "Design new UI component", "reward": 350},
        {"id": "b9", "title": "Write unit tests for service A", "reward": 200},
    ]

def load_seen_bounties(filepath):
    """Loads previously seen bounties from a JSON file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filepath}. Starting with empty seen bounties.")
        return []

def save_seen_bounties(filepath, bounties):
    """Saves the current list of seen bounties to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(bounties, f, indent=4)

# --- Main logic that needs fixing ---
def main():
    seen_bounties_filepath = 'seen_bounties.json'
    
    # 1. Load existing seen bounties
    seen_bounties = load_seen_bounties(seen_bounties_filepath)
    seen_bounty_ids = {bounty['id'] for bounty in seen_bounties}
    
    # 2. Fetch current bounties
    current_bounties = fetch_current_bounties()
    
    new_bounties = []
    for bounty in current_bounties:
        if bounty['id'] not in seen_bounty_ids:
            new_bounties.append(bounty)
    
    num_new_bounties = len(new_bounties)
    
    if num_new_bounties > 0:
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunityies found")
        
        # --- FIX: Ensure new bounties are added to the seen list before saving ---
        # The previous issue likely stemmed from 'seen_bounties' not being updated
        # with 'new_bounties' before being saved back to the file.
        # This caused the same bounties to be reported as new on every run.
        seen_bounties.extend(new_bounties) # ADDED LINE: Incorporate new bounties into the seen list
        save_seen_bounties(seen_bounties_filepath, seen_bounties) # Save the now updated list
        # --- END FIX ---
        
    else:
        print("No new bounties found.")

if __name__ == '__main__':
    main()
    