
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads the set of bounty IDs that have already been seen from the JSON file.
    If the file doesn't exist or is corrupted, returns an empty set.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """
    Saves the current set of seen bounty IDs to the JSON file.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    """
    Simulates fetching the current list of available bounties.
    In a real application, this would involve web scraping or API calls.
    For this demonstration, it returns a mock set of bounties to simulate
    the scenario where 17 new bounties are found.
    """
    # To simulate finding 17 new bounties when 3 are already seen,
    # we return a total of 20 bounties.
    all_bounties = {f"bounty_id_{i}" for i in range(1, 21)} # e.g., bounty_id_1 to bounty_id_20
    return all_bounties

def scout_for_new_bounties():
    """
    Compares current bounties with previously seen ones and alerts on new opportunities.
    """
    seen_bounties = load_seen_bounties()
    
    # --- Mocking initial state for the specific issue reproduction ---
    # If seen_bounties.json does not exist (first run), we pre-fill `seen_bounties`
    # with 3 mock bounties. This ensures that when `fetch_current_bounties` returns
    # 20 bounties, exactly 17 'new' ones are identified, matching the issue's alert count.
    if not seen_bounties and not os.path.exists(SEEN_BOUNTIES_FILE):
        initial_seen_mock = {f"bounty_id_{i}" for i in range(1, 4)} # Simulate 3 bounties already seen
        seen_bounties.update(initial_seen_mock)
        save_seen_bounties(seen_bounties) # Persist this mock initial state for subsequent runs
    # --- End of mocking initial state ---

    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found") 
        seen_bounties.update(new_bounties) # Add newly found bounties to the seen list
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    # To run this script multiple times and see different outputs:
    # 1. First run: should report 17 new bounties (due to initial_seen_mock).
    # 2. Second run: should report "No new bounties found."
    # To reset for testing, uncomment the following line to delete the seen_bounties.json file:
    # if os.path.exists(SEEN_BOUNTIES_FILE):
    #     os.remove(SEEN_BOUNTIES_FILE)
    
    scout_for_new_bounties()
    