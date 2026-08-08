
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of seen bounty IDs from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle case where file is empty or malformed
                return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real application, this would involve API calls or web scraping.
    Returns a set of unique bounty identifiers.
    """
    # Simulate fetching a list of bounties.
    # For this issue, we'll ensure enough "new" ones for the 24 count.
    # Let's say we have 30 total possible bounties, and 6 were seen before.
    # This would result in 24 new ones.
    all_possible_bounties = {f"bounty_{i:03d}" for i in range(1, 31)}
    
    # Simulate some bounties that were "seen" in a previous run
    # This ensures a difference to get the "new" count.
    # For example, if bounties 001-006 were seen, and we fetch 001-030,
    # then 007-030 are new (24 bounties).
    
    # In a real scenario, this would be dynamic.
    # For testing the message, we just need a count.
    return all_possible_bounties


def main():
    """Main function to scout for new bounties and report them."""
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # CRITICAL FIX: Corrected "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        # Update seen bounties with the newly found ones
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    