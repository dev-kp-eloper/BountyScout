
# Bounty Scout

This repository contains a Python script to scout for new bounties.

## Files

- `scout_bounties.py`: The main script for finding bounties.
- `seen_bounties.json`: Stores a list of bounties that have already been seen.

## Testing Bounty Alerts

To ensure the bounty alert mechanism functions correctly, especially regarding the count of new opportunities, follow these steps:

1.  **Prepare for a fresh run**:
    *   Make a backup of `seen_bounties.json` if you wish to preserve your existing data.
    *   Delete or empty `seen_bounties.json` (e.g., `echo "[]" > seen_bounties.json` in a Unix-like terminal) to simulate a first run or a scenario where no bounties have been seen yet.

2.  **Execute the scout script**:
    *   Run the main scouting script: `python scout_bounties.py`

3.  **Verify the alert**:
    *   Observe the console output. You should see an alert message similar to:
        `🎯 Bounty Alert: X New Opportunit(y/ies) found`
    *   The value `X` should reflect the number of new opportunities discovered during that run.
    *   To specifically test the scenario mentioned in issue #648 ("7 New Opportunities found"), you would need to ensure that the source of bounties (which `scout_bounties.py` fetches from) currently contains 7 items that are not in `seen_bounties.json` at the time of execution. You can manually manipulate `seen_bounties.json` and potentially the simulated output of `scout_bounties.py`'s fetching logic (if applicable) to achieve this specific count for testing purposes.

This procedure helps verify that the script correctly identifies new bounties and reports their count in the expected format.
    