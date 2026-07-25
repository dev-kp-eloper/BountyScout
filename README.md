# 🎯 BountyScout

Automated bug bounty opportunity finder that scouts multiple platforms and alerts you about new programs.

## Features

- 🔍 **Multi-Platform Scanning**: Monitors HackerOne, Bugcrowd, Intigriti, and YesWeHack
- 🤖 **Automated Alerts**: Creates GitHub issues when new bounties are found
- 📊 **Data Tracking**: Maintains history of all discovered bounties
- ⏰ **Scheduled Runs**: Automatically checks for new opportunities every 6 hours
- 💰 **Bounty Details**: Tracks company, bounty range, scope, and program URLs

## Setup

### Prerequisites

- Node.js 18 or higher
- GitHub repository with Actions enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dev-kp-eloper/BountyScout.git
cd BountyScout
```

2. Install dependencies:
```bash
npm install
```

3. Configure GitHub Actions:
   - The workflow is already configured in `.github/workflows/bounty-scout.yml`
   - It uses the default `GITHUB_TOKEN` for creating issues
   - No additional secrets needed!

## Usage

### Manual Run

Run the scout locally:
```bash
npm run scout
```

Create an issue from found bounties:
```bash
export GITHUB_TOKEN=your_token_here
npm run create-issue
```

### Automated Runs

The GitHub Action runs automatically:
- Every 6 hours via cron schedule
- Can be triggered manually from the Actions tab

### Data Storage

Bounty data is stored in:
- `data/bounties.json` - All discovered bounties
- `data/new-bounties.json` - Latest new bounties (temporary)

## Issue Format

When new bounties are found, an issue is created with:
- Total count of new opportunities
- Grouped by platform
- Details including:
  - Company name
  - Bounty range
  - Scope
  - Direct link to program
  - Discovery timestamp

## Customization

### Change Scan Frequency

Edit `.github/workflows/bounty-scout.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Change to your preferred schedule
```

### Add More Platforms

Edit `src/index.js` and add to the `PLATFORMS` array:
```javascript
{
  name: 'PlatformName',
  url: 'https://platform.com/programs',
  type: 'platform-id'
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is for educational and informational purposes. Always respect the terms of service of bug bounty platforms and follow responsible disclosure practices.

---

🤖 Happy Hunting! 🎯