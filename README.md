# BountyScout

Automated bounty opportunity scanner and tracker.

## Features

- Automated scanning for bounty opportunities across GitHub
- Daily issue creation with new findings
- Automatic cleanup of stale alerts (>24h)
- Organized tracking with labels and automation

## Automated Workflows

### Bounty Alert Lifecycle

1. **Creation**: New bounty alerts are posted as GitHub issues daily
2. **Labeling**: Automatically tagged with `bounty-alert` and `automated` labels
3. **Cleanup**: Issues older than 24 hours are automatically closed to prevent clutter

### Workflow Files

- `.github/workflows/label-bounty-alerts.yml` - Auto-labels new bounty alert issues
- `.github/workflows/close-bounty-alerts.yml` - Closes stale alerts daily at 05:00 UTC

## Manual Operations

To manually trigger the cleanup workflow:

```bash
gh workflow run close-bounty-alerts.yml
```

## Configuration

The cleanup workflow runs daily at 05:00 UTC (1 hour after typical scan time of 04:00 UTC). This ensures alerts are visible for approximately 24 hours before cleanup.

To adjust the schedule, edit the cron expression in `.github/workflows/close-bounty-alerts.yml`:

```yaml
schedule:
  - cron: '0 5 * * *'  # Runs at 05:00 UTC daily
```

## Labels

- `bounty-alert` - Automated bounty opportunity notifications
- `automated` - System-generated content

## License

MIT
