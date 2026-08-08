
import json
import os

def get_new_bounties():
    """Simulates finding new bounties."""
    # In a real scenario, this would involve scraping or API calls
    # For demonstration, let's return a fixed list if no seen bounties exist,
    # or an empty list if bounties were already "seen".
    try:
        with open('seen_bounties.json', 'r') as f:
            seen = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        seen = []
    
    potential_new = ["Bounty A", "Bounty B", "Bounty C", "Bounty D", "Bounty E", "Bounty F", "Bounty G", "Bounty H", "Bounty I", "Bounty J", "Bounty K", "Bounty L"]
    
    new_found = [b for b in potential_new if b not in seen]
    
    return new_found

def update_seen_bounties(bounties):
    """Adds new bounties to the seen_bounties.json file."""
    try:
        with open('seen_bounties.json', 'r+') as f:
            seen = json.load(f)
            f.seek(0) # Go to the beginning of the file to overwrite
    except (FileNotFoundError, json.JSONDecodeError):
        seen = []
    
    updated = False
    for bounty in bounties:
        if bounty not in seen:
            seen.append(bounty)
            updated = True
    
    if updated:
        json.dump(seen, f, indent=4)
        f.truncate() # Remove remaining part if new content is shorter
    elif not os.path.exists('seen_bounties.json'): # Create if it didn't exist and no new bounties
        with open('seen_bounties.json', 'w') as f:
            json.dump([], f, indent=4)


def main():
    new_bounties = get_new_bounties()
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        alert_message = f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found"
        print(alert_message)
        update_seen_bounties(new_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    