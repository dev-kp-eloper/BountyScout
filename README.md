# 🎯 BountyScout

Automated GitHub bounty opportunity finder that scans for open bounty issues across GitHub and notifies you of new opportunities.

## Features

- 🔍 Automatically searches for bounty-related issues across GitHub
- 💰 Extracts bounty amounts from issue descriptions
- 📊 Tracks bounties in a structured JSON format
- 🔔 Creates GitHub issues to notify about new bounties
- ⏰ Runs on a schedule via GitHub Actions
- 🚀 Zero configuration required

## How It Works

BountyScout searches GitHub for issues with:
- Bounty-related labels (bounty, bug-bounty, reward, etc.)
- Keywords in titles/descriptions ($, bounty, reward, prize)
- References to bounty platforms (Gitcoin, Bountysource, IssueHunt)

When new bounties are found, it:
1. Saves them to `data/bounties.json`
2. Creates a GitHub issue with a summary of new opportunities
3. Tracks the last run to avoid duplicates

## Setup

1. Fork this repository
2. Enable GitHub Actions in your fork
3. The workflow will run automatically every 6 hours
4. Check the Issues tab for bounty alerts!

### Manual Run

You can also trigger the workflow manually:
1. Go to the "Actions" tab
2. Select "Bounty Scout" workflow
3. Click "Run workflow"

## Data Structure

Bounties are stored in `data/bounties.json` with the following structure:

```json
{
  "bounties": [
    {
      "id": 123456789,
      "title": "Fix bug - $500 bounty",
      "url": "https://github.com/owner/repo/issues/123",
      "repository": "owner/repo",
      "author": "username",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "state": "open",
      "labels": ["bounty", "bug"],
      "amount": "$500",
      "body": "Issue description...",
      "comments": 5
    }
  ],
  "lastUpdated": "2024-01-01T00:00:00Z",
  "totalCount": 100,
  "newCount": 5
}
```

## Local Development

```bash
# Install dependencies
npm install

# Set GitHub token
export GITHUB_TOKEN=your_github_token

# Run the scout
npm start
```

## Configuration

The workflow runs every 6 hours by default. To change the schedule, edit `.github/workflows/bounty-scout.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Change this line
```

## Contributing

Contributions are welcome! Feel free to:
- Add new bounty platforms to search
- Improve bounty amount extraction
- Add filtering options
- Enhance the notification format

## License

MIT License - feel free to use this project however you'd like!

## Disclaimer

This tool is for informational purposes only. Always verify bounty details and legitimacy before working on any issue. The maintainers are not responsible for any disputes or issues arising from bounty opportunities found by this tool.
