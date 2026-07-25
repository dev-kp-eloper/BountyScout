# 🎯 BountyScout

Automated GitHub bounty opportunity scout that finds and tracks bug bounties, rewards, and paid issues across GitHub.

## Features

- 🔍 Automatically searches for bounty opportunities across GitHub
- 📊 Tracks new bounties and creates alerts
- 🤖 Runs on a schedule via GitHub Actions
- 💾 Maintains a database of discovered bounties
- 🎉 Creates issues for new opportunities

## How It Works

BountyScout searches GitHub for issues with bounty-related labels such as:
- `bounty`
- `bug-bounty`
- `reward`
- `hacktoberfest`
- `good first issue`
- `help wanted`
- `prize`
- `bounty-hunter`
- `cash-reward`

When new bounties are found, it:
1. Saves them to `data/bounties.json`
2. Creates a new issue with details about the opportunities
3. Updates the last run timestamp

## Setup

1. Fork this repository
2. Enable GitHub Actions in your fork
3. The workflow will run automatically every 6 hours
4. You can also trigger it manually from the Actions tab

## Manual Usage

```bash
# Install dependencies
npm install

# Set your GitHub token
export GITHUB_TOKEN=your_token_here

# Run the scout
npm start
```

## Configuration

The scout runs automatically via GitHub Actions. You can modify the schedule in `.github/workflows/bounty-scout.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
```

## Data Storage

All discovered bounties are stored in:
- `data/bounties.json` - Complete list of all bounties
- `data/last-run.json` - Metadata about the last run

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own bounty hunting!

## Disclaimer

This tool is for informational purposes only. Always verify bounty details and terms directly with the repository owners before starting work.
