# Bounty Alert Management

## Overview

BountyScout automatically creates issues for new bounty opportunities. To prevent accumulation of stale alerts, automated workflows manage the lifecycle of these issues.

## Automated Workflows

### 1. Labeling (`.github/workflows/label-bounty-alerts.yml`)

- **Trigger**: When a new issue is opened
- **Action**: Automatically adds `bounty-alert` and `automated` labels to issues with "🎯 Bounty Alert:" in the title
- **Purpose**: Enables filtering and automated cleanup

### 2. Stale Alert Cleanup (`.github/workflows/close-stale-bounty-alerts.yml`)

- **Trigger**: Every 6 hours (or manual dispatch)
- **Action**: Closes bounty alert issues older than 48 hours
- **Rationale**: Bounty opportunities are time-sensitive; 48-hour window allows review while preventing backlog

## Manual Management

### Viewing Active Alerts

```bash
# Filter by label
https://github.com/YOUR_ORG/BountyScout/issues?q=is%3Aissue+is%3Aopen+label%3Abounty-alert
```

### Adjusting Retention Period

Edit `.github/workflows/close-stale-bounty-alerts.yml`:

```yaml
# Change from 48 hours to desired duration
cutoffDate.setHours(cutoffDate.getHours() - 48);
```

### Disabling Auto-Cleanup

Remove or disable the scheduled trigger:

```yaml
on:
  # schedule:
  #   - cron: '0 */6 * * *'
  workflow_dispatch:  # Keep manual trigger only
```

## Best Practices

1. **Review alerts within 48 hours** - Opportunities expire quickly
2. **Pin important alerts** - Pinned issues are not auto-closed
3. **Use project boards** - Track bounties you're actively pursuing
4. **Subscribe to notifications** - Enable watching for bounty-alert label

## Troubleshooting

### Workflow Not Running

- Check Actions tab for execution history
- Verify repository has Actions enabled
- Ensure workflow has `issues: write` permission

### Too Many/Few Closures

- Adjust the 48-hour cutoff in the workflow
- Check issue creation rate vs. closure rate
- Consider adjusting cron schedule frequency
