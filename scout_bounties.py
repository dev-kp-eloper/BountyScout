
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads bounty IDs that have already been seen from a JSON file.
    Returns a set of seen bounty IDs.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with no seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def get_current_bounties():
    """
    Simulates fetching current bounty IDs from a source (e.g., a website or API).
    In a real application, this function would contain web scraping or API call logic.
    For this example, it returns a hardcoded set to simulate finding new bounties.
    """
    # Example bounties. Adjust this set to simulate different scenarios.
    # To simulate "4 New Opportunities found", we assume 4 of these are truly new
    # compared to what might be in seen_bounties.json from a previous run.
    return {
        "bounty_id_101",
        "bounty_id_102",
        "bounty_id_103",
        "bounty_id_104",
        "bounty_id_105", # Potentially new
        "bounty_id_106", # Potentially new
        "bounty_id_107", # Potentially new
        "bounty_id_108", # Potentially new
    }

def scout_bounties():
    """
    Main function to scout for new bounties, compare them with seen ones,
    report new opportunities, and update the seen bounties list.
    """
    print("Starting bounty scout...")
    seen_bounties = load_seen_bounties()
    current_bounties = get_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        num_new = len(new_bounties)
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {num_new} new bounties.")
    else:
        print("No new bounties found.")
    print("Bounty scout finished.")

if __name__ == "__main__":
    # Example setup for simulating the "4 new bounties" scenario:
    # If you want to test this, you might clear or pre-populate seen_bounties.json
    # before running. For instance, if seen_bounties contains 4 of the items
    # returned by get_current_bounties, then 4 new ones will be reported.

    # Uncomment the following lines to simulate an initial state where 4 bounties
    # are already seen, leading to 4 new ones being reported by `get_current_bounties`.
    # if os.path.exists(SEEN_BOUNTIES_FILE):
    #     os.remove(SEEN_BOUNTIES_FILE)
    # initial_seen_ids = {"bounty_id_101", "bounty_id_102", "bounty_id_103", "bounty_id_104"}
    # save_seen_bounties(initial_seen_ids)

    scout_bounties()
    