
import json
import os

def load_seen_bounties(filepath="seen_bounties.json"):
    """Loads a set of seen bounty IDs from a JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle case where file is empty or malformed
            return set()
    return set()

def save_seen_bounties(bounties, filepath="seen_bounties.json"):
    """Saves a set of bounty IDs to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(list(bounties), f, indent=4)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real application, this would scrape a website or query an API.
    """
    # For demonstration, let's return some mock bounties.
    # In a real scenario, this data would come from an external source.
    return {
        "bounty_id_alpha",
        "bounty_id_beta",
        "bounty_id_gamma",
        "bounty_id_delta",
        "bounty_id_epsilon",
        "bounty_id_zeta",
        "bounty_id_eta",
        "bounty_id_theta",
        "bounty_id_iota",
        "bounty_id_kappa"
    }

def scout_for_new_bounties():
    """
    Compares current bounties with previously seen bounties and reports new ones.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # Fix: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_new_bounties()
    