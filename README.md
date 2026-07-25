# 🎯 BountyScout

Automated GitHub bounty opportunity scanner that finds and alerts you about new bounty issues across GitHub.

## Features

- 🔍 Automatically scans GitHub for bounty opportunities
- 🏷️ Searches by labels and keywords
- 📊 Tracks scanned issues to avoid duplicates
- 🔔 Creates GitHub issues with new bounty alerts
- ⏰ Runs on a schedule (every 6 hours by default)
- 💰 Extracts reward information when available

## Setup

1. **Fork or clone this repository**

2. **Enable GitHub Actions**
   - Go to the "Actions" tab in your repository
   - Enable workflows if prompted

3. **Configure Secrets (Optional)**
   - The workflow uses `GITHUB_TOKEN` which is automatically provided
   - For higher rate limits, you can add a personal access token:
     - Go to Settings → Secrets and variables → Actions
     - Add a new secret named `GITHUB_TOKEN` with your personal access token

4. **Customize Search (Optional)**
   - Edit `src/index.js` to modify:
     - `BOUNTY_KEYWORDS`: Keywords to search for
     - `BOUNTY_LABELS`: Labels to search for
   - Edit `.github/workflows/bounty-scout.yml` to change the schedule

## How It Works

1. **Scheduled Scanning**: The workflow runs every 6 hours (configurable)
2. **Search Strategy**: Searches GitHub for issues with bounty-related labels and keywords
3. **Deduplication**: Maintains a cache of scanned issues to avoid duplicates
4. **Alert Creation**: Creates a new issue in your repository with details of found bounties
5. **Information Extraction**: Attempts to extract reward amounts and other relevant details

## Manual Trigger

You can manually trigger a scan:
1. Go to the "Actions" tab
2. Select "Bounty Scout" workflow
3. Click "Run workflow"

## Output Format

When new bounties are found, an issue is created with:
- Title: "🎯 Bounty Alert: X New Opportunities Found"
- Details for each bounty:
  - Repository name and link
  - Issue number and link
  - Reward amount (if detected)
  - Labels
  - Programming language

## Search Criteria

The scanner looks for issues with:
- **Labels**: bounty, bounties, reward, prize, gitcoin, hacktoberfest
- **Keywords**: bounty, reward, prize, hackathon, gitcoin, bountysource

## Rate Limiting

The scanner includes delays between API calls to respect GitHub's rate limits:
- 2 seconds between label searches
- 2 seconds between keyword searches
- Uses authenticated requests for higher limits

## Files

- `src/index.js`: Main scanner logic
- `.github/workflows/bounty-scout.yml`: GitHub Actions workflow
- `cache.json`: Stores scanned issue IDs (auto-generated)
- `results.json`: Stores latest scan results (auto-generated)

## Contributing

Contributions are welcome! Feel free to:
- Add new search strategies
- Improve reward extraction
- Add filtering options
- Enhance the alert format

## License

MIT License - feel free to use and modify as needed.

## Disclaimer

This tool is for informational purposes only. Always verify bounty details and legitimacy before participating. The scanner may not catch all bounties or may include false positives.