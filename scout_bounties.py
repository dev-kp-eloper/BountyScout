
import json
import os

# Assume some function to find new bounties
def find_new_bounties():
    # This is a placeholder. In a real scenario, it would fetch from an API or parse a website.
    # For demonstration, let's say it always finds 13 new bounties initially.
    # In a real script, it would compare against seen_bounties.json
    all_bounties = [f"bounty_{i}" for i in range(20)]
    
    seen_bounties_file = 'seen_bounties.json'
    seen_bounties_data = set()
    if os.path.exists(seen_bounties_file):
        with open(seen_bounties_file, 'r') as f:
            try:
                seen_bounties_data = set(json.load(f))
            except json.JSONDecodeError:
                # Handle empty or malformed JSON
                seen_bounties_data = set()

    new_bounties = [b for b in all_bounties if b not in seen_bounties_data]
    
    # Update seen bounties
    with open(seen_bounties_file, 'w') as f:
        json.dump(list(seen_bounties_data.union(set(all_bounties))), f, indent=2)

    return new_bounties

if __name__ == "__main__":
    new_opportunities = find_new_bounties()
    num_new = len(new_opportunities)
    if num_new > 0:
        # Corrected typo: "Opportunityies" -> "Opportunities"
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
    else:
        print("No new bounties found.")
    