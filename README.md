# 🎯 Bounty Scout: Hourly Notification System

A lightweight, state-tracking GitHub bounty scanner that runs **hourly**, searches for new open bounties, filters out competitive/crypto spam, and alerts you instantly.

Since it tracks seen bounty URLs, **it will only notify you once per bounty** (no spam).

---

## 🚀 How It Works

1. **GitHub Action Scheduled Trigger:** Runs automatically at minute `0` of every hour.
2. **Scouts GitHub:** Queries active bounty search keywords using the GitHub Search API.
3. **Triages Candidates:** Skips pull requests, already-assigned issues, overcrowded threads (>25 comments), and crypto-related spam.
4. **State Machine Comparison:** Composed against `seen_bounties.json` to extract strictly **new** opportunities.
5. **Instant Notifications:** Dispatches updates through your preferred channel (GitHub Issues, Telegram, or Discord).
6. **Persists State:** Saves the updated seen list back to the repository so you don't receive duplicate alerts on the next run.

---

## 🛠️ Step-by-Step Setup

### 1. Repository File Structure
```text
BountyScout/
├── .github/
│   └── workflows/
│       └── bounty-scout.yml      # GitHub Actions workflow (hourly schedule)
├── scout_bounties.py              # Core scout + notification script
├── seen_bounties.json             # Auto-created on first run (state persistence)
└── README.md
```

### 2. Choose Your Notification Method

#### 📬 Option A: Native GitHub Issues (Zero Setup - Recommended)
The script will automatically open a structured issue labeled `bounty-alert` in your own repository containing links to the new opportunities.
- **Why it's great:** Zero setup! You will get an email and/or mobile push notification directly from the GitHub app if you are watching your repository.
- **Setup:** None required. The built-in `GITHUB_TOKEN` handles everything.

---

#### 💬 Option B: Telegram Channel/Chat Alerts
The scout will send markdown alerts directly to your Telegram chat or channel.

1. **Create a Bot:** Message `@BotFather` on Telegram, send `/newbot`, and copy the **API Token**.
2. **Get your Chat ID:** Send a message to your new bot, then open `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates` in your browser. Look for `"chat":{"id":123456789}`. Copy that numeric ID.
3. **Add Secrets to GitHub:**
   - Go to your repository **Settings** > **Secrets and variables** > **Actions**.
   - Create a repository secret named `TELEGRAM_BOT_TOKEN` with your bot's token.
   - Create a repository secret named `TELEGRAM_CHAT_ID` with your numeric chat ID.

---

#### 🎮 Option C: Discord Channel Alerts
The scout will push formatted alerts directly to a channel in your Discord server.

1. **Create Webhook:** Go to your Discord server, click channel settings (gear icon) > **Integrations** > **Webhooks** > **Create Webhook**. Copy the Webhook URL.
2. **Add Secrets to GitHub:**
   - Go to your repository **Settings** > **Secrets and variables** > **Actions**.
   - Create a repository secret named `DISCORD_WEBHOOK_URL` with your webhook URL.

---

## 🧪 Triggering Manually
You can test the setup immediately without waiting for the next hour:
1. Go to your repository on GitHub.
2. Click on the **Actions** tab.
3. Select **Scout Active Bounties Hourly** from the sidebar.
4. Click the **Run workflow** dropdown and select **Run workflow**.

Happy bounty hunting! 🚀

---

## Spam Filters

Issues are dropped if they contain blocklisted keywords, match meta-notification title patterns (`Bounty Alert`, `New Opportunit…`), carry labels like `bounty-alert` / `honeypot-task`, or come from known farming repos (including other `*/bountyscout` forks and `zhangjiayang6835-cyber/ai-research`).

Edit `BLOCKLIST`, `TITLE_BLOCKLIST`, `LABEL_BLOCKLIST`, and `REPO_BLOCKLIST` in `scout_bounties.py` to tune.

### Disable GitHub Issue alerts

If hourly issue creation is too noisy, keep Telegram/Discord and set `BOUNTYSCOUT_GITHUB_ISSUES=0` in `.github/workflows/bounty-scout.yml`.
