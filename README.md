# BountyScout

GitHub bounty opportunity scanner.

## Features
- Scans multiple repositories for bounty issues
- Supports Discord and Telegram notifications
- Configurable scan targets

## Setup
1. Set `GITHUB_TOKEN` environment variable
2. Optionally set `DISCORD_WEBHOOK` and/or `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`
3. Run `npm start`

## Configuration
Edit `src/config.js` to add/remove scanned repositories.
