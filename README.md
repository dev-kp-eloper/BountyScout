# Bounty Scout: Hourly Notification System

A lightweight, state-tracking GitHub bounty scanner that runs **hourly**, searches for new open bounties, filters out competitive/crypto spam, and alerts you instantly.

Since it tracks seen bounty URLs, **it will only notify you once per bounty** (no spam).

---

## How It Works

1. **GitHub Action Scheduled Trigger:** Runs automatically at minute `0` of every hour.
2. **Scouts GitHub:** Queries active bounty search keywords using the GitHub Search API.
3. **Triages Candidates:** Skips pull requests, already-assigned issues, overcrowded threads (>25 comments), and crypto-related spam.
4. **State Machine Comparison:** Composed against `seen_bounties.json` to extract strictly **new** opportunities.
5. **Instant Notifications:** Dispatches updates through your preferred channel (GitHub Issues, Telegram, or Discord).
6. **Persists State:** Saves the updated seen list back to the repository so you don't receive duplicate alerts on the next run.

---

## Step-by-Step Setup

### 1. Repository File Structure