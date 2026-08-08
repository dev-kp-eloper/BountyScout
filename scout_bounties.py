
import json
import os
import random # For simulating new bounties

SEEN_BOUNTIES_FILE = "seen_bounties.json"

def load_seen_bounties():
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set() # Return empty set if file is corrupt
    return set()

def save_seen_bounties(seen_bounties):
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def fetch_bounties_mock():
    """
    Mocks fetching bounties. In a real scenario, this would hit an API.
    For demonstration, it returns a fixed list plus some random new ones.
    """
    base_bounties = [
        {"id": "bounty_1", "title": "Fix login bug", "value": 100},
        {"id": "bounty_2", "title": "Implement new feature X", "value": 250},
        {"id": "bounty_3", "title": "Optimize database query", "value": 150},
    ]
    
    # Simulate new bounties appearing over time
    new_bounties = []
    num_new = random.randint(0, 5) # Simulate 0 to 5 new bounties
    for i in range(num_new):
        new_bounties.append({"id": f"bounty_new_{random.randint(100, 999)}", 
                             "title": f"New Opportunity {i+1}", 
                             "value": random.randint(50, 300)})
    
    return base_bounties + new_bounties

def scout_for_bounties():
    print("Scouting for new bounties...")
    seen_bounties_ids = load_seen_bounties()
    
    current_bounties = fetch_bounties_mock()
    
    new_opportunities = []
    for bounty in current_bounties:
        if bounty['id'] not in seen_bounties_ids:
            new_opportunities.append(bounty)
            
    if new_opportunities:
        # Fixed typo: "Opportunityies" changed to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        for op in new_opportunities:
            print(f"  - {op['title']} (Value: ${op['value']})")
        
        # Add all current bounties to seen, so we don't re-alert on existing ones
        # and new ones are marked as seen.
        for bounty in current_bounties:
            seen_bounties_ids.add(bounty['id'])
        save_seen_bounties(seen_bounties_ids)
    else:
        print("No new bounties or opportunities found at this time.")

if __name__ == "__main__":
    scout_for_bounties()
    