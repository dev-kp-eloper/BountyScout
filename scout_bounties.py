
import json
import os

# Placeholder for actual bounty fetching logic
def get_current_bounties():
    # In a real scenario, this would scrape a website or API
    # For demonstration, let's return some dummy bounties to simulate finding 8 new ones
    # assuming some already exist in seen_bounties.json or initial run.
    # For simplicity, let's just return 8 "new" ones relative to an empty seen_bounties.json
    return ["bounty_1", "bounty_2", "bounty_3", "bounty_4", "bounty_5", "bounty_6", "bounty_7", "bounty_8"]

def load_seen_bounties(file_path="seen_bounties.json"):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle case where file is empty or malformed
                return set()
    return set()

def save_seen_bounties(bounties, file_path="seen_bounties.json"):
    with open(file_path, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = set(get_current_bounties())

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        # Update seen bounties
        save_seen_bounties(seen_bounties.union(current_bounties))
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    