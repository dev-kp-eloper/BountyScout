# BountyScout 🎯

Automated GitHub bounty opportunity finder that scouts for bug bounties, rewards, and other opportunities across GitHub.

## Features

- 🔍 Automatically searches for bounty opportunities across GitHub
- 📊 Tracks new bounties and prevents duplicates
- 🤖 Creates issues with new opportunities (with corrected spelling!)
- ⏰ Runs on a schedule via GitHub Actions
- 💾 Persists bounty data between runs

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up GitHub token:
   - The workflow uses `GITHUB_TOKEN` automatically
   - For local testing, set `GITHUB_TOKEN` environment variable

4. Run manually:
   ```bash
   npm start
   ```

## How It Works

1. Searches GitHub for issues with bounty-related labels and keywords
2. Compares found issues against previously tracked bounties
3. Creates a new issue in this repository with details about new opportunities
4. Automatically fixes the typo "Opportunityies" to "Opportunities"
5. Closes any old issues with the typo and creates corrected versions

## Configuration

The scout runs every 6 hours via GitHub Actions. You can also trigger it manually from the Actions tab.

## Data Storage

Bounty data is stored in `data/bounties.json` and committed to the repository.

## Contributing

Feel free to open issues or submit pull requests to improve BountyScout!

## License

MIT
