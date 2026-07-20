# BountyScout 🕵️

Automated GitHub bounty scanner that monitors multiple repositories for new bounty opportunities and creates GitHub Issues with the results.

## Features

- 🔍 Scans configured GitHub repositories for bounty-labeled issues
- 📊 Generates structured reports with bounty details
- 🏷️ Filters by bounty labels (e.g., "bounty", "MRWK bounty")
- 📝 Creates GitHub Issues with scan results
- 🧠 Tracks seen bounties to avoid duplicates
- ⏰ Runs on schedule via GitHub Actions

## Setup

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token with `repo` scope

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/BountyScout.git
   cd BountyScout
   ```

2. Install dependencies:
   ```bash
   pip install requests PyGithub
   ```

3. Configure environment variables:
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export TARGET_REPO="your-username/your-repo"  # Repository to post results to
   ```

### Configuration

Edit `scout_bounties.py` to configure:

- **`REPOSITORIES`**: List of repositories to scan (e.g., `["ramimbo/mergework", "mergeos-bounties/mergeos"]`)
- **`BOUNTY_LABELS`**: Labels to filter for (e.g., `["bounty", "MRWK bounty"]`)
- **`SEEN_FILE`**: Path to the JSON file tracking seen bounties

## Usage

### Local Run

```bash
python scout_bounties.py
```

### GitHub Actions

The workflow runs automatically every 6 hours. To trigger manually:

1. Go to your repository's **Actions** tab
2. Select **Bounty Scout** workflow
3. Click **Run workflow**

## Output

When new bounties are found, an Issue is created in the target repository with:

- **Title**: 🎯 Bounty Alert: N New Opportunities Found
- **Body**: Structured markdown with:
  - Scan timestamp
  - Bounty list with links, comments count, and last update time
  - Repository names for context

## Example Issue Output

```markdown
## Active Bounty Scan Results

**Scan Time:** 2026-05-26 15:42 UTC

#### 1. [MRWK bounty: review open MergeWork PRs with evidence, round 11](https://github.com/ramimbo/mergework/issues/404)
- **Repository:** [ramimbo/mergework](https://github.com/ramimbo/mergework)
- **Comments:** 11
- **Last Updated:** 2026-05-26T15:37:16Z
```

## Project Structure

```
BountyScout/
├── .github/
│   └── workflows/
│       └── bounty-scout.yml    # GitHub Actions workflow
├── scout_bounties.py           # Main scanner script
├── seen_bounties.json          # Tracked seen bounties (auto-generated)
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details
