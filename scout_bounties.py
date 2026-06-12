import json
import requests
from datetime import datetime

def load_seen_bounties(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_seen_bounties(filename, bounties):
    with open(filename, 'w') as file:
        json.dump(bounties, file, indent=4)

def fetch_bounty_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    seen_bounties = load_seen_bounties('seen_bounties.json')
    seen_bounty_urls = [bounty['url'] for bounty in seen_bounties]
    
    # Example scan results (in a real scenario, this would be fetched from somewhere)
    scan_results = [
        {"url": "https://github.com/SecureBananaLabs/bug-bounty/issues/6860", "last_updated": "2026-06-12T19:05:21Z"},
        # Add more scan results here...
    ]
    
    new_bounties = []
    for result in scan_results:
        if result['url'] not in seen_bounty_urls:
            new_bounties.append(result)
            seen_bounty_urls.append(result['url'])
            seen_bounties.append(result)
    
    save_seen_bounties('seen_bounties.json', seen_bounties)
    
    if new_bounties:
        # Create a new issue with the bounty alert
        print("Creating new issue with bounty alert...")
        # Logic to create a new issue goes here...

if __name__ == "__main__":
    main()