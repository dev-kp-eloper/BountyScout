
import json

def get_bounties_from_source():
    """
    This function would typically scrape a website or API to find current bounties.
    For demonstration, it returns a dummy list of bounties.
    In a real scenario, this would involve HTTP requests and parsing.
    """
    print("Scouting for bounties...")
    # Placeholder for actual bounty scraping logic
    # Example: return ["bounty_A", "bounty_B", "bounty_C", "bounty_D"]
    return ["bounty_123", "bounty_456", "bounty_789"] # Example bounties

def load_seen_bounties(filename="seen_bounties.json"):
    """Loads a set of previously seen bounty IDs from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"No existing {filename} found or file is empty/corrupt. Starting fresh.")
        return set()

def save_seen_bounties(bounties_set, filename="seen_bounties.json"):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(list(bounties_set), f, indent=2)

def main():
    """Main function to scout for new bounties and generate alerts."""
    current_bounties = set(get_bounties_from_source())
    seen_bounties = load_seen_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # This is the alert message that was identified with a typo.
        # FIX: Corrected "Opportunityies" to "Opportunities".
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        
        # In a real scenario, this might also trigger a GitHub API call
        # to create or update an issue with this title.

        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        print(f"Added {len(new_bounties)} new bounties to seen_bounties.json.")
    else:
        print("No new bounties found this run.")
        # If no new bounties, ensure the seen_bounties.json is still up-to-date
        # with any potentially new bounties that were previously found but not saved
        # in case of an error in a previous run.
        if current_bounties != seen_bounties:
             save_seen_bounties(current_bounties)


if __name__ == "__main__":
    main()
    