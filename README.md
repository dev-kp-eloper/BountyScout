# 🎯 BountyScout

Automated bounty opportunity finder that scouts multiple platforms for new bug bounties and opportunities.

## Features

- 🔍 Automatically searches multiple bounty platforms
- 🎯 Tracks new opportunities and creates GitHub issues
- 🤖 Runs on a schedule via GitHub Actions
- 📊 Maintains history of discovered bounties

## Supported Platforms

- GitHub (issues with bounty labels)
- Gitcoin

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up GitHub token:
   - The workflow uses `GITHUB_TOKEN` automatically
   - For local testing, create a `.env` file with:
     ```
     GITHUB_TOKEN=your_github_token
     ```

4. Enable GitHub Actions in your repository

## Usage

### Automated (GitHub Actions)

The bounty scout runs automatically every 6 hours via GitHub Actions. You can also trigger it manually:

1. Go to the "Actions" tab in your repository
2. Select "Bounty Scout" workflow
3. Click "Run workflow"

### Manual

Run locally:

```bash
node src/index.js
```

## How It Works

1. **Scout**: Searches configured platforms for bounty opportunities
2. **Compare**: Checks against previously discovered bounties
3. **Report**: Creates/updates a GitHub issue with new findings
4. **Track**: Saves bounty data for future comparisons

## Data Storage

Bounty data is stored in the `data/` directory:
- `bounties.json`: All discovered bounties
- `new-bounties.json`: Latest new bounties (used for issue creation)

## Configuration

Edit `src/index.js` to:
- Add new bounty platforms
- Adjust search parameters
- Modify filtering logic

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT