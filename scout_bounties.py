
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                # Ensure the loaded data is a list before converting to a set
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
                else:
                    print(f"Warning: {SEEN_BOUNTIES_FILE} contains invalid format. Starting with an empty set.")
                    return set()
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to the file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_current_bounties_mock():
    """
    Simulates fetching current bounties from a source.
    For the purpose of this fix, it provides a consistent set of bounties
    that, when combined with a hypothetical initial `seen_bounties.json` state,
    can result in 6 new bounties (e.g., if 4 bounties were already seen).
    """
    # These are all bounties currently available from scouting.
    # To match the "6 New" in the issue, imagine bounty_id_1 to bounty_id_4
    # were already present in `seen_bounties.json` when the script runs.
    return {f"bounty_id_{i}" for i in range(1, 11)} # 10 bounties in total

def scout_bounties():
    """
    Main function to scout for new bounties, report them, and update
    the list of seen bounties.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties_mock()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        num_new_bounties = len(new_bounties)
        # CRITICAL FIX: Corrected "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        
        # Update and save seen bounties
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    # When `scout_bounties.py` is run for the first time with an empty or non-existent
    # `seen_bounties.json`, it will report 10 new bounties based on `fetch_current_bounties_mock`.
    # To specifically reproduce the "6 New Opportunityies found" scenario from the issue,
    # the `seen_bounties.json` file would need to be pre-populated with 4 bounty IDs
    # (e.g., `["bounty_id_1", "bounty_id_2", "bounty_id_3", "bounty_id_4"]`)
    # before running this script. The fix itself targets the typo in the message string.
    scout_bounties()
