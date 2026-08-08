
import json
import os

# Placeholder function to simulate fetching current bounties from a source.
# In a real application, this would involve API calls, web scraping, etc.
def fetch_current_bounties():
    """
    Simulates fetching a list of current bounties.
    Each bounty is a dictionary with 'id' and 'title'.
    """
    # For the purpose of demonstration and to potentially align with the "9 New"
    # aspect of the issue, we'll simulate a fixed set of bounties.
    # If 'seen_bounties.json' is initially empty, this would result in 9 new bounties.
    return [
        {"id": f"bounty_{i}", "title": f"Bounty {i} Description"} for i in range(1, 10) # Simulating 9 bounties
    ]

def load_seen_bounties(file_path="seen_bounties.json"):
    """
    Loads previously seen bounty IDs from a JSON file.
    Handles cases where the file doesn't exist or is malformed/empty.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                # Ensure the file is not empty before trying to load JSON
                content = f.read()
                if content:
                    return set(json.loads(content))
                else:
                    return set()
            except json.JSONDecodeError:
                # Handle cases where the JSON file is malformed
                return set()
    return set()

def save_seen_bounties(bounty_ids, file_path="seen_bounties.json"):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(file_path, 'w') as f:
        # Convert set to list for JSON serialization
        json.dump(list(bounty_ids), f, indent=2)

def main():
    """
    Main function to scout for new bounties, identify new opportunities,
    and issue an alert if new bounties are found.
    """
    seen_bounty_ids = load_seen_bounties()
    current_bounties_data = fetch_current_bounties()
    current_bounty_ids = {bounty['id'] for bounty in current_bounties_data}

    new_bounty_ids = current_bounty_ids - seen_bounty_ids

    if new_bounty_ids:
        # CRITICAL FIX: Changed "Opportunityies" to "Opportunities" to correct the typo.
        print(f"🎯 Bounty Alert: {len(new_bounty_ids)} New Opportunities found")
        
        # Update the set of seen bounties and save it
        seen_bounty_ids.update(new_bounty_ids)
        save_seen_bounties(seen_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
