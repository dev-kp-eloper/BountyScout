# 🎯 BountyScout

Automated GitHub bounty opportunity finder that helps you discover and track bounty issues across GitHub.

## Features

- 🔍 Automatically searches for bounty opportunities across multiple platforms
- 📊 Tracks bounties from Gitcoin, Bountysource, IssueHunt, Algora, and more
- 🤖 Creates automated alerts for new opportunities
- 📈 Maintains a database of discovered bounties
- ⏰ Runs on a schedule (every 6 hours by default)

## How It Works

BountyScout uses GitHub Actions to:
1. Search for issues with bounty-related keywords
2. Filter out closed, invalid, or duplicate issues
3. Track new opportunities and store them in `data/bounties.json`
4. Create/update GitHub issues with alerts about new bounties

## Setup

1. Fork this repository
2. Enable GitHub Actions in your fork
3. The workflow will run automatically every 6 hours
4. Check the "Issues" tab for bounty alerts

## Manual Run

You can manually trigger the workflow:
1. Go to the "Actions" tab
2. Select "Bounty Scout" workflow
3. Click "Run workflow"

## Configuration

The scout searches for bounties using these platforms:
- **Gitcoin**: Issues mentioning "gitcoin bounty"
- **Bountysource**: Issues mentioning "bountysource"
- **IssueHunt**: Issues mentioning "issuehunt"
- **Algora**: Issues mentioning "algora bounty"
- **Generic**: Issues with "bounty", "reward", or "prize" in title and bounty label

## Data Structure

Bounty data is stored in `data/bounties.json` with the following structure:
```json
{
  "bounties": [
    {
      "id": 123456,
      "title": "Issue title",
      "url": "https://github.com/...",
      "repository": "owner/repo",
      "state": "open",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "labels": ["bounty"],
      "platform": "Gitcoin"
    }
  ],
  "last_updated": "2024-01-01T00:00:00Z",
  "stats": {
    "total": 100,
    "new": 5,
    "by_platform": {
      "Gitcoin": 20,
      "Generic": 80
    }
  }
}
```

## Contributing

Contributions are welcome! Feel free to:
- Add new bounty platforms
- Improve search queries
- Enhance filtering logic
- Add tests

## License

MIT
