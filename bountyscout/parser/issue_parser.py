import re
import json
from datetime import datetime

def parse_bounty_alert_markdown(markdown_body: str) -> list[dict]:
    """
    Parses a GitHub issue body markdown string to extract bounty details.

    Args:
        markdown_body: The full markdown content of a GitHub issue body.

    Returns:
        A list of dictionaries, where each dictionary represents a bounty
        with keys like 'title', 'url', 'repository_name', 'repository_url',
        'comments', and 'last_updated'.
    """
    bounties = []
    lines = markdown_body.strip().split('\n')
    current_bounty_block_lines = []
    
    # Flag to indicate when to start accumulating lines for bounty blocks
    start_parsing = False
    
    for line in lines:
        # A new bounty block starts with '#### X.'
        if line.startswith('#### '):
            start_parsing = True
            if current_bounty_block_lines:
                # Process the previously accumulated bounty block
                bounties.append(_parse_single_bounty_block('\n'.join(current_bounty_block_lines)))
            # Start a new block
            current_bounty_block_lines = [line]
        elif start_parsing:
            # Accumulate lines for the current bounty block
            current_bounty_block_lines.append(line)
            
    # Process the last accumulated bounty block after the loop finishes
    if current_bounty_block_lines:
        bounties.append(_parse_single_bounty_block('\n'.join(current_bounty_block_lines)))
            
    return bounties

def _parse_single_bounty_block(block: str) -> dict:
    """
    Parses a single markdown block representing a bounty.

    Args:
        block: A string containing the markdown for one bounty.

    Returns:
        A dictionary with extracted bounty details.
    """
    bounty = {}

    # Extract Title and URL
    title_url_match = re.search(r'#### \d+\. \[(.*?)\]\((.*?)\)', block)
    if title_url_match:
        bounty['title'] = title_url_match.group(1).strip()
        bounty['url'] = title_url_match.group(2).strip()

    # Extract Repository Name and URL
    repo_match = re.search(r'- \*\*Repository:\*\* \[(.*?)\]\((.*?)\)', block)
    if repo_match:
        bounty['repository_name'] = repo_match.group(1).strip()
        bounty['repository_url'] = repo_match.group(2).strip()

    # Extract Comments count
    comments_match = re.search(r'- \*\*Comments:\*\* (\d+)', block)
    if comments_match:
        bounty['comments'] = int(comments_match.group(1))
    else:
        bounty['comments'] = 0 # Default to 0 if not found

    # Extract Last Updated timestamp
    last_updated_match = re.search(r'- \*\*Last Updated:\*\* (.*)', block)
    if last_updated_match:
        timestamp_str = last_updated_match.group(1).strip()
        try:
            # Replace 'Z' with '+00:00' for robust ISO 8601 parsing across Python versions
            bounty['last_updated'] = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).isoformat()
        except ValueError:
            bounty['last_updated'] = timestamp_str # Fallback to raw string if parsing fails
    else:
        bounty['last_updated'] = None # Default to None if not found

    return bounty
