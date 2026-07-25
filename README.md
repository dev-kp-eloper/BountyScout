# 🎯 BountyScout

Automated bounty opportunity finder that scans GitHub for bounty-related issues and sends notifications.

## Features

- 🔍 Automatically searches GitHub for bounty opportunities
- 🏷️ Finds issues with bounty-related labels
- 💰 Detects monetary rewards in issue descriptions
- 📢 Sends notifications via Discord and/or Slack
- 💾 Tracks previously found bounties to avoid duplicates
- ⏰ Runs on a schedule via GitHub Actions

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dev-kp-eloper/BountyScout.git
   cd BountyScout
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

   Required:
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token

   Optional:
   - `DISCORD_WEBHOOK_URL`: Discord webhook for notifications
   - `SLACK_WEBHOOK_URL`: Slack webhook for notifications

4. **Run locally**
   ```bash
   npm start
   ```

## GitHub Actions Setup

The workflow runs automatically every 6 hours. To set it up:

1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `GITHUB_TOKEN` (automatically provided by GitHub)
   - `DISCORD_WEBHOOK_URL` (optional)
   - `SLACK_WEBHOOK_URL` (optional)

## How It Works

1. **Search**: Scans GitHub for issues with bounty-related labels and keywords
2. **Filter**: Identifies issues with monetary rewards or bounty indicators
3. **Compare**: Checks against previously found bounties
4. **Notify**: Sends alerts for new opportunities via configured channels
5. **Store**: Saves found bounties to avoid duplicate notifications

## Notification Format

Notifications include:
- Issue title and link
- Repository name
- Author
- Labels
- Description preview
- Creation timestamp

## License

MIT