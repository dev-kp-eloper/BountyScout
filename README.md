# BountyScout 🕵️

Automated GitHub bounty scanner that monitors repositories for new bounty opportunities and posts them as issues.

## Features

- 🔍 Scans multiple GitHub repositories for bounty-labeled issues
- 📝 Automatically creates summary issues with all found bounties
- 🧠 Remembers previously seen bounties to avoid duplicates
- ⏰ Runs on a configurable schedule via GitHub Actions

## Setup

1. **Fork this repository**
2. **Add a GitHub Token** as a repository secret named `GH_TOKEN` with `public_repo` scope
3. **Configure target repositories** in `scout_bounties.py`:
   - Edit the `REPOS` list to include repositories you want to monitor
   - Each entry should be in the format `"owner/repo"`
4. **Customize the schedule** in `.github/workflows/bounty-scout.yml` if needed

## How It Works

1. The workflow runs on a schedule (default: every 6 hours) or can be triggered manually
2. `scout_bounties.py` queries each configured repository for issues labeled with "bounty"
3. New bounties are collected and formatted into a summary
4. A new issue is created in this repository with the bounty report
5. Previously seen bounties are tracked in `seen_bounties.json` to prevent duplicates

## Configuration

### Target Repositories

Edit the `REPOS` list in `scout_bounties.py`:

```python
REPOS = [
    "owner1/repo1",
    "owner2/repo2",
]
```

### Scan Schedule

Edit the cron expression in `.github/workflows/bounty-scout.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

## Manual Trigger

You can also manually trigger a scan from the Actions tab in your repository.

## Output

Each scan creates a new issue with:
- Scan timestamp
- List of new bounty opportunities with links
- Repository names and comment counts
- Last update timestamps

## License

MIT
