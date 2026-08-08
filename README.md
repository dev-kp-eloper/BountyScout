
# Bounty Scout

This repository contains scripts and data for scouting and tracking bounties.

- `scout_bounties.py`: The main script for identifying new bounties.
- `seen_bounties.json`: Stores a list of bounties that have already been reported to prevent duplicate alerts.

## How to use

Run `scout_bounties.py` to check for new bounty opportunities.

```bash
python scout_bounties.py
```

The script will output an alert if new bounties are found and update `seen_bounties.json` accordingly.
    