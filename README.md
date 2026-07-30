# Bounty Hunter

Automated bounty opportunity scanner for GitHub issues.

## Features

- Scans multiple repositories for bounty-tagged issues
- Runs automatically every 6 hours
- Posts results to issue #640
- Tracks comments and last update times

## Configuration

The scanner monitors these repositories:
- akiver/cs-demo-manager
- opentoonz/opentoonz
- mergeos-bounties/Lappa
- attogram/rogue-blueberry

To add more repositories, edit `.github/workflows/bounty-scan.yml`.

## Manual Trigger

Go to Actions → Bounty Scanner → Run workflow

## How It Works

1. Searches for open issues containing bounty keywords
2. Filters by recent activity
3. Aggregates results with metadata
4. Posts formatted report to tracking issue

## Keywords Detected

- bounty
- reward
- prize
- Currency symbols: €, $, £
