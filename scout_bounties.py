
import json
import os
import requests # Assuming the script might fetch from a URL
from datetime import datetime

# Configuration
SEEN_BOUNTIES_FILE = 'seen_bounties.json'
BOUNTY_SOURCE_URL = 'https://example.com/api/bounties' # Placeholder for actual source

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                content = f.read()
                if content: # Check if file is not empty
                    return set(json.loads(content))
                else:
                    print(f"Info: {SEEN_BOUNTIES_FILE} is empty. Starting fresh.")
                    return set()
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting fresh.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def fetch_current_bounties():
    """
    Fetches the latest bounties from a source (e.g., an API or website).
    Returns a set of unique bounty identifiers.
    """
    try:
        print(f"Fetching bounties from {BOUNTY_SOURCE_URL}...")
        
        # Placeholder for actual fetching logic.
        # In a real scenario, this would involve web scraping or an API call, e.g.:
        # response = requests.get(BOUNTY_SOURCE_URL)
        # response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        # data = response.json()
        # return {item['id'] for item in data.get('bounties', [])}
        
        # For demonstration purposes to simulate "3 New Opportunities found":
        # Let's assume some existing bounties in seen_bounties.json and some new ones here.
        # If seen_bounties.json starts empty, these will all be new.
        all_bounties_today = {
            'bounty-abc-123',
            'bounty-def-456',
            'bounty-ghi-789', # Potentially new
            'bounty-jkl-012', # Potentially new
            'bounty-mno-345'  # Potentially new
        }
        return all_bounties_today
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return set()

def scout_bounties():
    """
    Main function to scout for new bounties, report them, and update the seen list.
    """
    print(f"Starting bounty scout at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    if not current_bounties:
        print("No current bounties could be fetched. Exiting.")
        return

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        num_new_bounties = len(new_bounties)
        
        # MODIFIED: Fix misspelling "Opportunityies" to "Opportunities"
        # MODIFIED: Add pluralization logic for "Opportunity" vs "Opportunities"
        opportunity_word = "Opportunity" if num_new_bounties == 1 else "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New {opportunity_word} found")
        
        # Update the set of seen bounties and save
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {num_new_bounties} new bounties.")
    else:
        print("No new bounties found since last check.")

if __name__ == "__main__":
    scout_bounties()
    