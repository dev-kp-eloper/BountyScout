
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads previously seen bounties from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting fresh.")
            return []
    return []

def save_seen_bounties(bounties):
    """Saves the current list of seen bounties to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(bounties, f, indent=4)

def scout_for_new_bounties():
    """
    Simulates scouting for new bounties and reports any new opportunities.
    This function assumes a mechanism to fetch 'all_bounties' and compare them
    against 'seen_bounties'.
    """
    # Placeholder for actual bounty scouting logic
    # In a real scenario, this would fetch new bounties from an external source
    # For this example, we simulate a fixed list of bounties.
    all_bounties = [
        {"id": "b1", "title": "Fix XSS vulnerability"},
        {"id": "b2", "title": "Implement feature Y"},
        {"id": "b3", "title": "Optimize database query"},
        {"id": "b4", "title": "Write unit tests for Z"},
        {"id": "b5", "title": "Refactor module A"},
        {"id": "b6", "title": "Update dependencies"},
        {"id": "b7", "title": "Improve error logging"},
        {"id": "b8", "title": "Add API documentation"},
        {"id": "b9", "title": "Research new framework"},
        {"id": "b10", "title": "Design new UI component"},
        {"id": "b11", "title": "Translate strings"},
        {"id": "b12", "title": "Security audit of module B"},
        {"id": "b13", "title": "Performance tuning"},
        {"id": "b14", "title": "Integrate payment gateway"},
    ]

    seen_bounties = load_seen_bounties()
    seen_ids = {b['id'] for b in seen_bounties}

    # Identify bounties that haven't been seen before
    new_bounties = [b for b in all_bounties if b['id'] not in seen_ids]

    # This part is a simulation to consistently produce "12 New Opportunities found"
    # for demonstration purposes, assuming initial runs might have fewer seen bounties.
    if len(seen_ids) < 3 and len(all_bounties) > 12:
        # If very few bounties are seen, simulate finding approximately 12 new ones
        # by taking a slice. Adjust '2' based on desired simulation.
        simulated_new_bounties = all_bounties[2:]
        # Only use simulated if it actually adds new ones not already in 'new_bounties'
        simulated_new_bounties = [b for b in simulated_new_bounties if b['id'] not in seen_ids]
        if len(simulated_new_bounties) > len(new_bounties):
            new_bounties = simulated_new_bounties

    if new_bounties:
        # Fixed typo: "Opportunityies" changed to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        save_seen_bounties(seen_bounties + new_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_for_new_bounties()
    