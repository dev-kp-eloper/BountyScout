
import json
import os

# Placeholder for actual bounty scouting logic.
# In a real scenario, this would scrape websites, APIs, etc.
def scout_for_new_bounties():
    # Simulate finding 8 new bounties for demonstration purposes,
    # matching the "8 New Opportunityies found" in the issue description.
    # In a real application, this would return actual bounty data (e.g., dicts).
    return [f"bounty_id_{i}" for i in range(1, 9)]

def main():
    seen_bounties_file = 'seen_bounties.json'
    
    # Load previously seen bounties
    if os.path.exists(seen_bounties_file):
        try:
            with open(seen_bounties_file, 'r') as f:
                # Assuming seen_bounties.json stores a list of unique bounty identifiers
                seen_bounties = set(json.load(f))
        except json.JSONDecodeError:
            # Handle case where seen_bounties.json might be empty or corrupted
            print(f"Warning: {seen_bounties_file} is corrupted or empty. Starting with no seen bounties.")
            seen_bounties = set()
    else:
        seen_bounties = set()

    # Scout for new bounties
    # Convert to set for efficient comparison
    all_found_bounties = set(scout_for_new_bounties())

    # Determine truly new bounties by subtracting already seen ones
    new_opportunities = all_found_bounties - seen_bounties

    if new_opportunities:
        # Update seen bounties with the newly found ones
        updated_seen_bounties = seen_bounties.union(new_opportunities)
        with open(seen_bounties_file, 'w') as f:
            # Save the updated set back to JSON as a list
            json.dump(list(updated_seen_bounties), f, indent=4)
        
        # CRITICAL CHANGE: Corrected the typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    