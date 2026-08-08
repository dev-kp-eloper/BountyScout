
import json
import os

# Define the file for storing seen bounties
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def scout_for_bounties():
    """
    Placeholder for the actual bounty scouting logic.
    This function would typically fetch bounties from external sources.
    For the purpose of demonstrating the fix, it simulates finding bounties.
    """
    # In a real scenario, this would involve API calls, web scraping, etc.
    # For this demonstration, we simulate finding 5 new bounties,
    # as suggested by the issue title "5 New Opportunityies found".
    # The message generation logic below will handle any count.
    
    # Example: Simulating some found bounties.
    # These could be fetched from an external API or parsed from a website.
    # Let's return a list of hypothetical bounty IDs.
    return [f"bounty_id_{i}" for i in range(1, 10)] # Simulate finding 9 bounties, some might be new, some seen.


def main():
    """Main function to scout for new bounties and generate an alert."""
    seen_bounties = load_seen_bounties()
    
    # Get the latest list of bounties from the scouting mechanism
    current_bounties = scout_for_bounties()
    
    new_bounty_ids = []
    updated_seen_bounties = set(seen_bounties) # Create a mutable copy

    for bounty_id in current_bounties:
        if bounty_id not in seen_bounties:
            new_bounty_ids.append(bounty_id)
            updated_seen_bounties.add(bounty_id)
            
    # Save the updated list of seen bounties
    save_seen_bounties(updated_seen_bounties)

    num_new_bounties = len(new_bounty_ids)

    # --- START OF MODIFIED ALERT MESSAGE GENERATION ---
    # This section replaces the previous, likely simpler, f-string for the alert.
    # It corrects the typo "Opportunityies" and handles pluralization and zero count.
    
    alert_suffix = ""
    if num_new_bounties == 0:
        alert_suffix = "No New Opportunities found"
    elif num_new_bounties == 1:
        alert_suffix = "1 New Opportunity found"
    else:
        alert_suffix = f"{num_new_bounties} New Opportunities found"
    
    final_alert_title = f"🎯 Bounty Alert: {alert_suffix}"
    
    # This is where the alert would typically be logged, printed, or used to create a GitHub issue.
    print(final_alert_title)
    # --- END OF MODIFIED ALERT MESSAGE GENERATION ---

if __name__ == "__main__":
    main()
    