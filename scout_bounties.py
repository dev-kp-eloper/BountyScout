
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads bounties that have already been seen from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                # Ensure it's a list, even if the file is empty or malformed
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    print(f"Warning: {SEEN_BOUNTIES_FILE} content is not a list. Starting fresh.")
                    return []
            except json.JSONDecodeError:
                print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting fresh.")
                return []
    return []

def save_seen_bounties(bounties):
    """Saves the current list of seen bounties to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(bounties, f, indent=2)

def fetch_current_bounties_simulation():
    """
    Simulates fetching current bounties from an external source.
    In a real-world scenario, this would involve an API call or web scraping.
    For demonstration purposes, it returns a fixed list of bounties.
    """
    current_opportunities = [
        {"id": "bounty_1", "title": "Implement user authentication", "value": "100 USD"},
        {"id": "bounty_2", "title": "Fix critical UI bug on checkout", "value": "75 USD"},
        {"id": "bounty_3", "title": "Add analytics tracking", "value": "120 USD"},
        {"id": "bounty_4", "title": "Optimize image loading performance", "value": "90 USD"},
        {"id": "bounty_5", "title": "Develop new API endpoint for reports", "value": "150 USD"},
        # Additional bounties could be added here over time in a real scenario
        # e.g., {"id": "bounty_6", "title": "Integrate payment gateway", "value": "300 USD"},
    ]
    return current_opportunities

def main():
    print("Scouting for new bounties...")

    # Load previously seen bounties
    seen_bounties = load_seen_bounties()
    seen_bounty_ids = {bounty['id'] for bounty in seen_bounties}

    # Simulate fetching current bounties
    current_bounties = fetch_current_bounties_simulation()

    # Identify new bounties
    new_bounties = []
    for bounty in current_bounties:
        if bounty['id'] not in seen_bounty_ids:
            new_bounties.append(bounty)

    if new_bounties:
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunit{'y' if len(new_bounties) == 1 else 'ies'} found")
        for bounty in new_bounties:
            print(f"  - {bounty['title']} (ID: {bounty['id']}) - Value: {bounty['value']}")
        
        # Add new bounties to the seen list and save
        seen_bounties.extend(new_bounties)
        save_seen_bounties(seen_bounties)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {len(new_bounties)} new bounties.")
    else:
        print("No new bounties found this run.")


if __name__ == "__main__":
    main()
    