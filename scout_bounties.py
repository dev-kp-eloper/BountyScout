
import json
import os
import time

# Configuration
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounty_ids):
    """Saves the current set of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounty_ids), f, indent=4)

def fetch_bounties_from_source():
    """
    Simulates fetching new bounties from an external source.
    In a real scenario, this would involve API calls, web scraping, etc.
    """
    print("Fetching bounties from external source...")
    # Simulate some new bounties
    mock_bounties = [
        {"id": "github-101", "title": "Implement dark mode", "url": "https://github.com/org/repo/issues/101"},
        {"id": "bounty-platform-202", "title": "Refactor authentication module", "url": "https://bounty.platform/task/202"},
        {"id": "gh-718-fix", "title": "Fix typo in bounty alert message", "url": "https://github.com/org/repo/issues/718"}
    ]
    # Add some previously seen bounties to test filtering
    seen_mock_bounties = [
        {"id": "old-bounty-1", "title": "Old task 1"},
        {"id": "github-101", "title": "Implement dark mode"} # Duplicate to show it's filtered
    ]
    return mock_bounties + seen_mock_bounties # Intentionally include a duplicate for testing logic

def main():
    """Main function to scout for new bounties and alert."""
    print(f"Starting bounty scout at {time.ctime()}...")

    seen_bounty_ids = load_seen_bounties()
    current_bounties_from_source = fetch_bounties_from_source()

    new_opportunities = []
    new_opportunity_ids = set()

    for bounty in current_bounties_from_source:
        bounty_id = bounty.get('id')
        if bounty_id and bounty_id not in seen_bounty_ids:
            new_opportunities.append(bounty)
            new_opportunity_ids.add(bounty_id)
            print(f"Found new bounty: {bounty.get('title')} ({bounty_id})")

    if new_opportunities:
        # Fixed typo: "Opportunityies" changed to "Opportunities"
        print(f"\n🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        for op in new_opportunities:
            print(f"- {op.get('title')} (ID: {op.get('id')}) - {op.get('url', 'No URL provided')}")
        
        # Update and save seen bounties
        seen_bounty_ids.update(new_opportunity_ids)
        save_seen_bounties(seen_bounty_ids)
        print(f"\nUpdated {SEEN_BOUNTIES_FILE} with {len(new_opportunity_ids)} new bounty IDs.")
    else:
        print("\nNo new bounties found this run.")

    print(f"Scout finished at {time.ctime()}.")

if __name__ == "__main__":
    main()
    