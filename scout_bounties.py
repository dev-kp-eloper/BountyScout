
import json
import requests
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'
BOUNTY_API_URL = 'https://api.example.com/bounties' # Placeholder API - Replace with actual API endpoint

def fetch_bounties_from_api():
    """Fetches bounties from a predefined API endpoint."""
    try:
        response = requests.get(BOUNTY_API_URL, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return []

def load_seen_bounties(filepath):
    """Loads previously seen bounties from a JSON file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {filepath} is corrupted or empty. Starting with an empty list of seen bounties.")
        return []
    except IOError as e:
        print(f"Error loading {filepath}: {e}")
        return []

def save_seen_bounties(filepath, bounties):
    """Saves the current list of seen bounties to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(bounties, f, indent=2)
    except IOError as e:
        print(f"Error saving {filepath}: {e}")

def main():
    """Main function to scout for new bounties and report them."""
    fetched_bounties = fetch_bounties_from_api()
    if not fetched_bounties:
        print("Could not fetch any bounties.")
        return

    seen_bounties = load_seen_bounties(SEEN_BOUNTIES_FILE)
    
    new_bounties = []
    # Create a set of IDs from seen bounties for efficient lookup
    seen_ids = {b.get('id') for b in seen_bounties if b.get('id')} 
    
    for bounty in fetched_bounties:
        bounty_id = bounty.get('id')
        if bounty_id and bounty_id not in seen_ids:
            new_bounties.append(bounty)
            seen_ids.add(bounty_id) # Add to seen_ids to prevent re-adding if API returns duplicates in one fetch

    if new_bounties:
        # Update seen_bounties by merging new bounties with existing ones.
        # Using a dictionary to ensure uniqueness by ID before converting back to a list.
        # This handles cases where bounties might appear in both `seen_bounties` and `new_bounties` (though `new_bounties` should ideally only contain truly new ones).
        updated_seen_bounties_dict = {b['id']: b for b in seen_bounties}
        updated_seen_bounties_dict.update({b['id']: b for b in new_bounties})
        updated_seen_bounties = list(updated_seen_bounties_dict.values())
        
        save_seen_bounties(SEEN_BOUNTIES_FILE, updated_seen_bounties)
        
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    