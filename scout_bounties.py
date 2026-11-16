import os
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Environment configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('GITHUB_REPOSITORY_OWNER')
REPO_NAME = os.getenv('GITHUB_REPOSITORY').split('/')[-1] if os.getenv('GITHUB_REPOSITORY') else None
API_BASE = 'https://api.github.com'

# Path to the JSON file that stores already processed bounty IDs
SEEN_BOUNTIES_PATH = Path(__file__).parent / 'seen_bounties.json'

def load_seen_bounties() -> List[str]:
    """Load the list of already processed bounty IDs.

    Returns:
        A list of bounty IDs (strings). If the file does not exist or is malformed,
        an empty list is returned and the file is recreated on write.
    """
    if not SEEN_BOUNTIES_PATH.exists():
        logger.info('Seen bounties file not found, initializing empty list.')
        return []
    try:
        with SEEN_BOUNTIES_PATH.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return [str(item) for item in data]
            else:
                logger.warning('Seen bounties file malformed, resetting.')
                return []
    except Exception as e:
        logger.error(f'Failed to read seen bounties: {e}')
        return []

def save_seen_bounties(bounty_ids: List[str]) -> None:
    """Persist the list of processed bounty IDs atomically.

    Args:
        bounty_ids: List of bounty IDs to store.
    """
    try:
        temp_path = SEEN_BOUNTIES_PATH.with_suffix('.tmp')
        with temp_path.open('w', encoding='utf-8') as f:
            json.dump(bounty_ids, f, indent=2)
        temp_path.replace(SEEN_BOUNTIES_PATH)
        logger.info('Seen bounties updated successfully.')
    except Exception as e:
        logger.error(f'Failed to write seen bounties: {e}')
        raise

def fetch_bounties() -> List[Dict[str, Any]]:
    """Fetch the latest bounty alerts from the external service.

    This function is a placeholder; replace the URL and parsing logic with the
    actual API used by the project.
    """
    # Example placeholder URL – in real usage replace with the actual endpoint
    BOUNTY_API_URL = 'https://example.com/api/bounties/latest'
    try:
        response = requests.get(BOUNTY_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Assume the API returns a list of objects with at least an 'id' and 'title'
        return data if isinstance(data, list) else []
    except Exception as e:
        logger.error(f'Error fetching bounties: {e}')
        return []

def create_github_issue(title: str, body: str) -> bool:
    """Create a new GitHub issue in the repository.

    Returns True on success, False otherwise.
    """
    if not all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME]):
        logger.error('Missing required GitHub environment variables.')
        return False
    url = f'{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json'
    }
    payload = {'title': title, 'body': body}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f'Created issue "{title}"')
        return True
    except Exception as e:
        logger.error(f'Failed to create issue "{title}": {e}')
        return False

def main() -> None:
    seen = set(load_seen_bounties())
    bounties = fetch_bounties()
    new_ids = []

    for bounty in bounties:
        bounty_id = str(bounty.get('id'))
        if not bounty_id:
            continue
        if bounty_id in seen:
            continue
        title = bounty.get('title', f'Bounty Alert: {bounty_id}')
        body = bounty.get('description', 'No description provided.')
        # Include a link if present
        link = bounty.get('url')
        if link:
            body += f"\n\n[View bounty]({link})"
        if create_github_issue(title, body):
            new_ids.append(bounty_id)
        else:
            logger.warning(f'Skipping persistence for bounty {bounty_id} due to issue creation failure.')

    if new_ids:
        # Merge new IDs with previously seen ones and persist
        all_ids = list(seen.union(new_ids))
        save_seen_bounties(all_ids)
    else:
        logger.info('No new bounties detected.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted by user')
        sys.exit(0)
    except Exception as exc:
        logger.exception(f'Unhandled exception: {exc}')
        sys.exit(1)
