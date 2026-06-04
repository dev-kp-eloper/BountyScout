# 🎯 BountyScout

Automated bug bounty scanner that monitors GitHub Issues for new bounty opportunities.

## Features

- Scans multiple GitHub repositories for open bug bounty issues
- Tracks previously seen bounties to avoid duplicates
- Generates formatted bounty alerts with issue details
- Supports configurable scan intervals via GitHub Actions

## Quick Start

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token (with `public_repo` scope)

### Installation

```bash
git clone https://github.com/your-username/BountyScout.git
cd BountyScout
pip install -r requirements.txt
```

### Configuration

1. Set the `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN="your_github_token_here"
```

2. (Optional) Edit `scout_bounties.py` to customize target repositories.

### Usage

Run the scanner manually:

```bash
python scout_bounties.py
```

Or set up GitHub Actions (see `.github/workflows/bounty-scout.yml`) to run on a schedule.

## How It Works

1. The scanner fetches open issues from configured repositories.
2. It filters for bounty-labeled issues (label: "bounty" or title containing "bounty").
3. New bounties (not in `seen_bounties.json`) are reported.
4. The `seen_bounties.json` file is updated to prevent duplicate alerts.

## Example Output

```
🎯 Bounty Alert: 3 New Opportunities found

Scan Time: 2026-06-03 23:47 UTC

1. [Payment API should require authentication](https://github.com/org/repo/issues/1)
   - Repository: org/repo
   - Comments: 2
   - Last Updated: 2026-06-03T23:46:35Z

2. [Add rate limiting to endpoints](https://github.com/org/repo/issues/2)
   - Repository: org/repo
   - Comments: 0
   - Last Updated: 2026-06-03T22:00:00Z
```

## Project Structure

```
BountyScout/
├── .github/
│   └── workflows/
│       └── bounty-scout.yml   # GitHub Actions workflow
├── scout_bounties.py          # Main scanner script
├── seen_bounties.json         # Tracks already-reported bounties
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
