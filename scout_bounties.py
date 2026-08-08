
import json
import os
import sys

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads a list of seen bounty IDs from the tracking file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
                return []
    return []

def save_seen_bounties(bounty_ids):
    """Saves the updated list of seen bounty IDs to the tracking file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(bounty_ids, f, indent=2)

def scout_for_new_bounties():
    """
    Simulates scouting for new bounties.
    In a real application, this would involve fetching data from external sources.
    Returns a list of dictionaries, where each dict represents a bounty.
    """
    print("Scouting for new bounties...")
    # Mock data for demonstration purposes
    return [
        {"id": "mock_bounty_1", "title": "Implement feature X", "url": "http://example.com/bounty1"},
        {"id": "mock_bounty_2", "title": "Fix bug Y in module Z", "url": "http://example.com/bounty2"},
        {"id": "mock_bounty_3", "title": "Optimize database query", "url": "http://example.com/bounty3"},
        {"id": "mock_bounty_4", "title": "Write API documentation", "url": "http://example.com/bounty4"},
        {"id": "mock_bounty_5", "title": "Refactor authentication module", "url": "http://example.com/bounty5"}
    ]

def find_new_opportunities(all_bounties, seen_bounty_ids):
    """
    Compares all found bounties against the list of seen bounty IDs
    to identify truly new opportunities.
    """
    new_bounties = []
    for bounty in all_bounties:
        if bounty['id'] not in seen_bounty_ids:
            new_bounties.append(bounty)
    return new_bounties

# NEW HELPER FUNCTION: Encapsulates the logic for generating the alert message.
def _generate_bounty_alert_message(count):
    """
    Generates the bounty alert message with correct pluralization.
    Fixes the typo 'Opportunityies' to 'Opportunities'.
    """
    if count == 1:
        return f"🎯 Bounty Alert: {count} New Opportunity found"
    else:
        # FIX: Changed "Opportunityies" to "Opportunities"
        return f"🎯 Bounty Alert: {count} New Opportunities found"

# NEW FUNCTION: Self-tests the bounty alert message generation.
def _run_self_tests():
    """
    Executes internal self-tests to verify the correctness of
    the bounty alert message generation, including pluralization and typo fix.
    """
    print("\n--- Running self-tests for bounty alert messages ---")

    # Test case 1: Plural form (e.g., 5 opportunities)
    test_count_plural = 5
    expected_plural_message = f"🎯 Bounty Alert: {test_count_plural} New Opportunities found"
    actual_plural_message = _generate_bounty_alert_message(test_count_plural)
    assert actual_plural_message == expected_plural_message, \
        f"Self-test failed for plural message (count={test_count_plural}): Expected '{expected_plural_message}', Got '{actual_plural_message}'"
    print(f"Self-test passed for plural message: '{actual_plural_message}'")

    # Test case 2: Singular form (e.g., 1 opportunity)
    test_count_singular = 1
    expected_singular_message = f"🎯 Bounty Alert: {test_count_singular} New Opportunity found"
    actual_singular_message = _generate_bounty_alert_message(test_count_singular)
    assert actual_singular_message == expected_singular_message, \
        f"Self-test failed for singular message (count={test_count_singular}): Expected '{expected_singular_message}', Got '{actual_singular_message}'"
    print(f"Self-test passed for singular message: '{actual_singular_message}'")

    # Test case 3: Zero bounties (should still use plural form if called with 0)
    test_count_zero = 0
    expected_zero_message = f"🎯 Bounty Alert: {test_count_zero} New Opportunities found"
    actual_zero_message = _generate_bounty_alert_message(test_count_zero)
    assert actual_zero_message == expected_zero_message, \
        f"Self-test failed for zero message (count={test_count_zero}): Expected '{expected_zero_message}', Got '{actual_zero_message}'"
    print(f"Self-test passed for zero message: '{actual_zero_message}'")

    print("--- All self-tests passed ---")

def main(run_tests=False):
    """
    Main function to run the bounty scout or self-tests.
    """
    if run_tests:
        _run_self_tests()
        return # Exit after running tests

    seen_bounty_ids = load_seen_bounties()
    all_bounties = scout_for_new_bounties()
    new_opportunities = find_new_opportunities(all_bounties, seen_bounty_ids)

    if new_opportunities:
        count = len(new_opportunities)
        # Use the new helper function to generate the message
        message = _generate_bounty_alert_message(count)
        print(message)

        # Update seen bounties with the IDs of the newly found ones
        for bounty in new_opportunities:
            if bounty['id'] not in seen_bounty_ids: # Prevent adding duplicates if any exist
                seen_bounty_ids.append(bounty['id'])
        save_seen_bounties(seen_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    # Check for a specific command-line argument to run tests
    if "--test" in sys.argv:
        main(run_tests=True)
    else:
        main(run_tests=False)
