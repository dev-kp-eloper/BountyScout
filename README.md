# 🎯 BountyScout

Automated bug bounty opportunity scout that monitors multiple platforms and alerts you to new opportunities.

## Features

- 🔍 Monitors multiple bug bounty platforms (HackerOne, Bugcrowd, Intigriti)
- 🤖 Automated scanning every 6 hours
- 📊 Tracks discovered bounties to avoid duplicates
- 🎯 Creates GitHub issues for new opportunities
- 📈 Organizes bounties by platform and severity

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure GitHub Actions:
   - The workflow runs automatically every 6 hours
   - You can also trigger it manually from the Actions tab

4. Ensure the repository has the following permissions:
   - Settings → Actions → General → Workflow permissions
   - Select "Read and write permissions"

## Usage

### Automated (Recommended)

The GitHub Action runs automatically on schedule. New bounties will be reported as GitHub issues.

### Manual

Run locally:
```bash
node src/index.js
```

Create an issue from the report:
```bash
export GITHUB_TOKEN=your_token_here
node src/create-issue.js
```

## Data Storage

Bounties are stored in `data/bounties.json` to track what has already been discovered.

## Issue Format

When new bounties are found, an issue is created with:
- Total count of new opportunities
- Organized by platform
- Details including reward, severity, and links
- Summary statistics

## Configuration

Edit `src/index.js` to:
- Add more bounty platforms
- Adjust scanning logic
- Customize bounty filtering

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own bounty hunting!

## Disclaimer

This tool is for educational purposes. Always respect the terms of service of bug bounty platforms and follow responsible disclosure practices.