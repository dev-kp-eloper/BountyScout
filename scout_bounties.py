import json
import requests
from datetime import datetime
import os

def load_seen_bounties():
    try:
        with open('seen_bounties.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_seen_bounties(bounties):
    with open('seen_bounties.json', 'w') as file:
        json.dump(bounties, file, indent=4)

def scan_for_bounties():
    # Example logic for scanning bounties; actual implementation may vary
    url = "https://api.github.com/search/issues?q=label:bounty+state:open"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        bounties = []
        for item in data['items']:
            bounty = {
                'repository': item['repository_url'],
                'title': item['title'],
                'comments': item['comments'],
                'last_updated': item['updated_at'],
                'url': item['html_url']
            }
            bounties.append(bounty)
        return bounties
    else:
        return []

def main():
    seen_bounties = load_seen_bounties()
    seen_bounty_urls = [bounty['url'] for bounty in seen_bounties]
    
    new_bounties = scan_for_bounties()
    new_bounty_urls = [bounty['url'] for bounty in new_bounties]
    
    # Check for new bounties
    really_new_bounties = [bounty for bounty in new_bounties if bounty['url'] not in seen_bounty_urls]
    
    if really_new_bounties:
        print(f"Found {len(really_new_bounties)} new bounties.")
        seen_bounties.extend(really_new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()