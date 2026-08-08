
import json
import requests
import time
import os # Added for test file cleanup
import sys # Added for command-line argument parsing

SEEN_BOUNTIES_FILE = 'seen_bounties.json'
BOUNTY_SOURCE_URL = 'https://api.example.com/bounties' # Placeholder, replace with actual URL

# Helper function to get the correct seen bounties file path
# This allows tests to use a temporary file
def get_seen_bounties_file_path(is_test=False):
    return 'test_seen_bounties.json' if is_test else SEEN_BOUNTIES_FILE

def load_seen_bounties(is_test=False):
    file_path = get_seen_bounties_file_path(is_test)
    try:
        with open(file_path, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen_bounties(seen_bounties, is_test=False):
    file_path = get_seen_bounties_file_path(is_test)
    with open(file_path, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties():
    """Fetches current bounties from the configured source."""
    try:
        response = requests.get(BOUNTY_SOURCE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return []

# MODIFIED: Added current_bounties_data parameter for testing and is_test flag
def scout_for_new_bounties(current_bounties_data=None, is_test=False):
    """
    Scouts for new bounties by comparing current bounties with previously seen ones.
    
    Args:
        current_bounties_data (list, optional): A list of bounty dictionaries to use
                                                 instead of fetching from URL. Used for testing.
        is_test (bool): If True, uses a separate 'test_seen_bounties.json' file.
    
    Returns:
        list: A list of newly found bounties.
    """
    seen_bounties = load_seen_bounties(is_test)
    
    if current_bounties_data is None: # Use real data if not provided (normal operation)
        current_bounties_data = fetch_current_bounties()

    new_bounties = []
    current_bounty_ids = set()

    for bounty in current_bounties_data:
        bounty_id = bounty.get('id') # Assuming each bounty has an 'id'
        if bounty_id:
            current_bounty_ids.add(bounty_id)
            if bounty_id not in seen_bounties:
                new_bounties.append(bounty)

    # Update seen bounties to include all current bounties
    seen_bounties.update(current_bounty_ids)
    save_seen_bounties(seen_bounties, is_test)

    return new_bounties

# NEW: Test function to verify bounty scouting logic
def run_scout_test_scenario():
    print("\n--- Running Bounty Scout Test Scenario ---")
    
    # Define the temporary file for testing
    test_seen_file = get_seen_bounties_file_path(is_test=True)

    # Helper to clean up the test seen bounties file
    def cleanup_test_file():
        if os.path.exists(test_seen_file):
            os.remove(test_seen_file)
            print(f"  - Cleaned up {test_seen_file}")

    # Ensure a clean slate before starting tests
    cleanup_test_file()
    
    try:
        # Scenario 1: Initial run with 3 bounties (all should be new)
        print("Scenario 1: Initial run with 3 bounties (all new)")
        initial_bounties = [
            {'id': 'b1', 'title': 'Test Bounty One'},
            {'id': 'b2', 'title': 'Test Bounty Two'},
            {'id': 'b3', 'title': 'Test Bounty Three'}
        ]
        new_ops_s1 = scout_for_new_bounties(current_bounties_data=initial_bounties, is_test=True)
        
        assert len(new_ops_s1) == 3, f"Test Failed (S1): Expected 3 new bounties, got {len(new_ops_s1)}"
        print(f"  - Initial run found {len(new_ops_s1)} new bounties. PASSED.")

        # Scenario 2: Some existing bounties, 2 new ones appear
        print("\nScenario 2: Adding 2 more new bounties")
        updated_bounties = [
            {'id': 'b1', 'title': 'Test Bounty One'},
            {'id': 'b2', 'title': 'Test Bounty Two'},
            {'id': 'b3', 'title': 'Test Bounty Three'},
            {'id': 'b4', 'title': 'Test Bounty Four'},
            {'id': 'b5', 'title': 'Test Bounty Five'}
        ]
        new_ops_s2 = scout_for_new_bounties(current_bounties_data=updated_bounties, is_test=True)
        
        assert len(new_ops_s2) == 2, f"Test Failed (S2): Expected 2 new bounties, got {len(new_ops_s2)}"
        print(f"  - Second run found {len(new_ops_s2)} new bounties. PASSED.")

        # Scenario 3: No new bounties (all already seen)
        print("\nScenario 3: No new bounties added")
        no_new_bounties = [
            {'id': 'b1', 'title': 'Test Bounty One'},
            {'id': 'b2', 'title': 'Test Bounty Two'},
            {'id': 'b3', 'title': 'Test Bounty Three'},
            {'id': 'b4', 'title': 'Test Bounty Four'},
            {'id': 'b5', 'title': 'Test Bounty Five'}
        ]
        new_ops_s3 = scout_for_new_bounties(current_bounties_data=no_new_bounties, is_test=True)

        assert len(new_ops_s3) == 0, f"Test Failed (S3): Expected 0 new bounties, got {len(new_ops_s3)}"
        print(f"  - Third run found {len(new_ops_s3)} new bounties. PASSED.")
        
        # Scenario 4: Simulating the specific issue: 8 new opportunities found
        print("\nScenario 4: Simulating 8 new opportunities (like issue #720)")
        # Clear test_seen_bounties.json to simulate a fresh start or a specific scenario
        cleanup_test_file() 
        
        eight_new_bounties = []
        for i in range(1, 9): # Generate 8 bounties
            eight_new_bounties.append({'id': f'issue720_bounty_{i}', 'title': f'Issue 720 Bounty {i}'})
        
        new_ops_s4 = scout_for_new_bounties(current_bounties_data=eight_new_bounties, is_test=True)
        
        assert len(new_ops_s4) == 8, f"Test Failed (S4): Expected 8 new bounties, got {len(new_ops_s4)}"
        print(f"  - Fourth run found {len(new_ops_s4)} new bounties. PASSED (simulating issue #720).")

        print("\n--- All Bounty Scout Test Scenarios Completed Successfully ---")

    except AssertionError as e:
        print(f"\n!!! TEST FAILED: {e} !!!")
    finally:
        cleanup_test_file()


if __name__ == "__main__":
    if '--test' in sys.argv:
        run_scout_test_scenario()
    else:
        print("Scouting for new bounties...")
        new_opportunities = scout_for_new_bounties()
        if new_opportunities:
            print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunityies found")
            for op in new_opportunities:
                print(f"- {op.get('title', 'No Title')} (ID: {op.get('id', 'N/A')})")
        else:
            print("No new opportunities found.")
    
    