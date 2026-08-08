
import json
import os
import time # Added for simulating real-world delays or logging timestamps

# Configuration
SEEN_BOUNTIES_FILE = 'seen_bounties.json'
MOCK_BOUNTIES_DATA = [
    {"id": "b001", "title": "Fix a critical bug in user authentication"},
    {"id": "b002", "title": "Implement new dashboard widget for analytics"},
    {"id": "b003", "title": "Optimize image loading performance on product pages"},
    {"id": "b004", "title": "Add multi-language support to the frontend"},
    {"id": "b005", "title": "Refactor legacy API endpoints to use GraphQL"},
    {"id": "b006", "title": "Develop a new feature for user profile management"},
    {"id": "b007", "title": "Integrate with a third-party payment gateway"},
    {"id": "b008", "title": "Create automated end-to-end tests for checkout flow"},
    {"id": "b009", "title": "Update documentation for developer API"},
    {"id": "b010", "title": "Design a new mobile app onboarding experience"}, # This would be a new one
    {"id": "b011", "title": "Improve accessibility for web application"}      # Another new one
]

def load_seen_bounties():
    """Loads bounty IDs that have already been seen from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with no seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def scout_for_bounties():
    """
    Simulates scouting for bounties. In a real application, this would involve
    web scraping, API calls, etc.
    For this example, it returns a subset of MOCK_BOUNTIES_DATA to simulate
    new bounties appearing over time.
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scouting for new bounties...")
    # Simulate some bounties being available at a given time
    # Let's say initially we have 7 bounties, and then more appear later.
    # For this run, let's return a subset that results in 7 *new* opportunities
    # if we assume some were already seen.
    # E.g., if seen_bounties.json contains ["b001", "b002"],
    # and MOCK_BOUNTIES_DATA[:9] is returned, then 7 new bounties will be found.
    return MOCK_BOUNTIES_DATA[:9] # Return first 9 mock bounties

def main():
    """Main function to scout for bounties and alert on new ones."""
    seen_bounty_ids = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = []
    current_bounty_ids_set = set()

    for bounty in current_bounties:
        bounty_id = bounty['id']
        current_bounty_ids_set.add(bounty_id)
        if bounty_id not in seen_bounty_ids:
            new_bounties.append(bounty)

    new_bounties_count = len(new_bounties)

    if new_bounties_count > 0:
        if new_bounties_count == 1:
            opportunity_word = "Opportunity"
        else:
            # FIX: Corrected typo from "Opportunityies" to "Opportunities"
            opportunity_word = "Opportunities" # Original: "Opportunityies"
        print(f"🎯 Bounty Alert: {new_bounties_count} New {opportunity_word} found")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] No new bounties found.")

    # Update the list of seen bounties
    # This ensures that these bounties won't be alerted again in the next run
    save_seen_bounties(current_bounty_ids_set)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Updated seen bounties. Total seen: {len(current_bounty_ids_set)}")

if __name__ == "__main__":
    main()
    