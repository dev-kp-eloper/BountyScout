# BountyScout 🎯

Automated bounty hunting scout for GitHub issues. Automatically discovers and tracks bounty opportunities across GitHub repositories.

## Features

- 🔍 Automatically searches for bounty-related issues across GitHub
- 📊 Tracks discovered bounties and prevents duplicates
- 🤖 Creates automated alerts when new bounties are found
- ⏰ Runs on a schedule via GitHub Actions
- 💾 Persistent storage of bounty data

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dev-kp-eloper/BountyScout.git
   cd BountyScout
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your GitHub Personal Access Token
   ```bash
   cp .env.example .env
   ```

4. **Run locally**
   ```bash
   npm start
   ```

## GitHub Actions Setup

The workflow is automatically configured to run every 6 hours. It will:
1. Search for new bounty opportunities
2. Store them in the data directory
3. Create an issue with new findings

### Required Secrets

The `GITHUB_TOKEN` is automatically provided by GitHub Actions. No additional secrets are needed.

## How It Works

1. **Search Phase**: Scans GitHub for issues containing bounty-related keywords
2. **Filter Phase**: Validates and deduplicates bounty opportunities
3. **Storage Phase**: Saves bounties to persistent storage
4. **Alert Phase**: Creates GitHub issues with new bounty opportunities

## Bounty Detection

The scout looks for these keywords:
- bounty
- reward
- $ (dollar signs)
- 💰 (money emoji)
- 🎯 (target emoji)
- prize
- compensation

## Data Storage

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
      "labels": ["bounty"],
      "found_at": "2024-01-01T00:00:00Z"
    }
  ],
  "lastChecked": "2024-01-01T00:00:00Z",
  "newCount": 5
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is for informational purposes only. Always verify bounty details and legitimacy before participating in any bounty program.