# Bounty Plaza

Automated bounty opportunity tracking and notification system.

## Features

- Automated daily scans for new bounty opportunities
- GitHub issue notifications for new bounties
- Automatic cleanup of stale bounty alerts

## Workflows

### Bounty Scanner
Runs daily at 04:00 UTC to scan for new bounty opportunities across configured repositories.

### Stale Alert Cleanup
Runs daily at 00:00 UTC to close bounty alert issues older than 24 hours.

## Configuration

Bounty alerts are automatically labeled with:
- `bounty` - Indicates a bounty-related issue
- `automated` - Indicates an automatically generated issue

## Manual Trigger

Both workflows can be manually triggered via the Actions tab in GitHub.

## Issue Management

Bounty alert issues (#581 and similar) are automatically:
1. Created when new opportunities are found
2. Closed after 24 hours to prevent clutter
3. Labeled for easy filtering and management

To prevent future automated bounty alerts, disable the "Bounty Scanner" workflow in the Actions tab.
