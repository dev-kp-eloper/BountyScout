# BountyScout 🎯

A GitHub Actions-powered bot that scans for active bug bounty opportunities across multiple platforms and posts them as issues.

## Features

- 🔍 **Automated Scanning**: Runs on a schedule (every 6 hours) to find new bounty opportunities
- 📊 **Rich Issue Formatting**: Creates well-structured GitHub issues with severity, repository info, and links
- 🧠 **Duplicate Detection**: Tracks previously seen bounties to avoid duplicate issues
- 🌐 **Multi-Platform Support**: Scans HackerOne, Bugcrowd, GitHub Advisory Database, and more
- 📈 **Severity Filtering**: Only posts bounties above a configurable severity threshold

## How It Works

1. The workflow runs on a cron schedule or can be triggered manually
2. `scout_bounties.py` fetches bounty data from configured sources
3. New bounties are compared against `seen_bounties.json` to avoid duplicates
4. A new GitHub Issue is created for each qualifying bounty opportunity

## Setup

### Prerequisites

- A GitHub repository with Actions enabled
- A GitHub Personal Access Token (PAT) with `repo` and `issues` scopes

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/BountyScout.git
   cd BountyScout
   ```

2. Add your GitHub token as a repository secret:
   - Go to Settings → Secrets and variables → Actions
   - Add a new secret named `GITHUB_TOKEN` with your PAT

3. Customize the scan sources in `scout_bounties.py` (optional)

### Configuration

Edit `scout_bounties.py` to configure:
- `SOURCES`: List of bounty platforms to scan
- `MIN_SEVERITY`: Minimum severity score (0-10) to report
- `SCAN_INTERVAL`: How often to scan (default: 6 hours)

## Usage

### Automatic Scanning

The workflow runs automatically every 6 hours. To trigger manually:

1. Go to the Actions tab
2. Select "Bounty Scout" workflow
3. Click "Run workflow" → "Run workflow"

### Viewing Results

- New bounty opportunities appear as Issues in this repository
- Each issue contains:
  - Bounty title and severity score
  - Link to the original bounty page
  - Repository and package information
  - Number of comments and last update timestamp

## Example Output

```
🎯 Bounty Alert: 16 New Opportunities found

**Scan Time:** 2026-06-03 18:47 UTC

#### 1. [axios-0.27.2.tgz: 25 vulnerabilities (highest severity is: 8.7) reachable](https://github.com/example/repo/issues/25)
- **Repository:** example/repo
- **Comments:** 0
- **Last Updated:** 2026-06-03T18:43:56Z
```

## Development

### Running Locally

```bash
python scout_bounties.py
```

### Testing

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)

## Disclaimer

This tool is for educational and research purposes only. Always follow the terms of service of the platforms you scan.