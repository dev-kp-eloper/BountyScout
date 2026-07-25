# 🎯 BountyScout

Automated bug bounty opportunity finder that scouts multiple platforms and alerts you about new opportunities.

## Features

- 🔍 Automatically scans multiple bug bounty platforms
- 🚨 Creates GitHub issues for new opportunities
- ⏰ Runs on a schedule via GitHub Actions
- 📊 Tracks bounty history to avoid duplicates
- 💰 Shows bounty ranges and program details

## Supported Platforms

- HackerOne
- Bugcrowd
- Intigriti
- YesWeHack

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Run manually:
   ```bash
   npm run scout
   ```

## GitHub Actions

The workflow automatically runs every 6 hours and:
1. Scans all supported platforms for bounties
2. Compares with previously found bounties
3. Creates a GitHub issue if new opportunities are found

### Manual Trigger

You can manually trigger the workflow from the Actions tab in GitHub.

## Configuration

The scout runs automatically via GitHub Actions. No additional configuration is needed.

## Data Storage

Bounty data is stored in the `data/` directory:
- `bounties.json` - All discovered bounties
- `new-bounties.json` - Newly discovered bounties (temporary)

## Development

### Project Structure

```
BountyScout/
├── .github/
│   └── workflows/
│       └── bounty-scout.yml
├── src/
│   ├── index.js          # Main scout logic
│   └── create-issue.js   # GitHub issue creator
├── data/                 # Bounty data storage
├── package.json
└── README.md
```

### Adding New Platforms

Edit `src/index.js` and add new platforms to the `PLATFORMS` array:

```javascript
{
  name: 'PlatformName',
  url: 'https://platform.com/programs',
  type: 'platform-id'
}
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and informational purposes. Always follow the terms of service of bug bounty platforms and respect program rules.