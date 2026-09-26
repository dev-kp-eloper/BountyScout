import json
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Bounty:
    title: str
    repo: str
    url: str
    last_updated: str
    comments: int

def parse_bounties(raw_text: str) -> List[Bounty]:
    """Parses bounty data from the provided markdown structure."""
    bounties = []
    # Regex to capture the bounty line and subsequent details
    pattern = re.compile(r"\[(?P<title>.*?)\]\((?P<url>.*?)\)\n- **Repository:** \[(?P<repo>.*?)\]\(.*?\)\n- **Comments:** (?P<comments>\d+)\n- **Last Updated:** (?P<updated>.*?)Z")
    
    for match in pattern.finditer(raw_text):
        bounties.append(Bounty(
            title=match.group("title"),
            repo=match.group("repo"),
            url=match.group("url"),
            last_updated=match.group("updated"),
            comments=int(match.group("comments"))
        ))
    return bounties

def export_to_json(bounties: List[Bounty], filename: str = "bounties.json"):
    """Exports parsed bounties to a structured JSON file."""
    with open(filename, 'w') as f:
        json.dump([b.__dict__ for b in bounties], f, indent=4)

if __name__ == "__main__":
    # Input provided via task description
    raw_input = """...""" # Placeholder for the full task description block
    
    try:
        parsed_data = parse_bounties(raw_input)
        export_to_json(parsed_data)
        print(f"Successfully processed {len(parsed_data)} bounties to bounties.json")
    except Exception as e:
        print(f"Error processing bounty list: {e}")