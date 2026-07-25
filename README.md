# 🎯 BountyScout

Automated GitHub bounty opportunity finder that scouts for new bounty issues across GitHub and notifies you about them.

## Features

- 🔍 Searches GitHub for bounty opportunities using multiple keywords and labels
- 🔔 Creates automated issue notifications for new bounties
- 📊 Tracks previously found bounties to avoid duplicates
- ⚡ Runs automatically on a schedule via GitHub Actions
- 🎨 Clean, organized bounty reports with repository info and previews

## How It Works

BountyScout searches GitHub for issues with:
- **Labels**: bounty, bug-bounty, reward, prize, hackathon, good first issue, help wanted, up-for-grabs
- **Keywords**: bounty, reward, prize, hackathon, bug bounty, security bounty, good first issue, help wanted

When new opportunities are found, it creates an issue in your repository with all the details.

## Setup

1. Fork or clone this repository
2. Enable GitHub Actions in your repository settings
3. The workflow will run automatically every 6 hours
4. You can also trigger it manually from the Actions tab

## Configuration

The bot uses the built-in `GITHUB_TOKEN` for authentication. No additional setup required!

## Manual Usage

```bash
# Install dependencies
npm install

# Run the scout
GITHUB_TOKEN=your_token node src/index.js
```

## Data Storage

Bounty data is stored in `data/bounties.json` to track previously found opportunities.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Note

**Fixed Issue**: The typo "Opportunityies" in issue titles has been corrected to "Opportunities" in the latest version.
