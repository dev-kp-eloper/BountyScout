# BountyScout 🎯

Automated bounty opportunity discovery and notification system.

## Features

- 🔍 Automated scanning for new bounty opportunities
- 📢 Multi-channel notifications (Console, Slack, Discord)
- ✅ Proper pluralization in notifications
- 🧪 Comprehensive test coverage
- 🛡️ Error handling and validation

## Installation

```bash
npm install
```

## Usage

### Basic Usage

```javascript
const NotificationService = require('./src/services/notificationService');

const notifier = new NotificationService({
  enabled: true,
  channels: ['console']
});

// Send notification about new opportunities
await notifier.sendBountyAlert(13, [
  {
    title: 'XSS Vulnerability',
    description: 'Find XSS vulnerabilities',
    reward: '$500',
    platform: 'HackerOne',
    url: 'https://example.com/bounty/1'
  }
]);
```

### Slack Integration

```javascript
const notifier = new NotificationService({
  channels: ['slack'],
  slackWebhookUrl: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
});

await notifier.sendBountyAlert(13, opportunities);
```

### Discord Integration

```javascript
const notifier = new NotificationService({
  channels: ['discord'],
  discordWebhookUrl: 'https://discord.com/api/webhooks/YOUR/WEBHOOK/URL'
});

await notifier.sendBountyAlert(13, opportunities);
```

### Multiple Channels

```javascript
const notifier = new NotificationService({
  channels: ['console', 'slack', 'discord'],
  slackWebhookUrl: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
  discordWebhookUrl: 'https://discord.com/api/webhooks/YOUR/WEBHOOK/URL'
});

await notifier.sendBountyAlert(13, opportunities);
```

## Notification Format

The notification system automatically handles proper pluralization:

- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 13 New Opportunities found"

## Testing

```bash
npm test
```

## Configuration

### NotificationService Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable notifications |
| `channels` | array | `['console']` | Notification channels to use |
| `slackWebhookUrl` | string | `undefined` | Slack webhook URL |
| `discordWebhookUrl` | string | `undefined` | Discord webhook URL |

## Opportunity Object Structure

```javascript
{
  title: string,        // Opportunity title
  description: string,  // Opportunity description
  reward: string,       // Reward amount
  platform: string,     // Platform name (e.g., 'HackerOne', 'Bugcrowd')
  url: string          // URL to the opportunity
}
```

## Error Handling

The notification service includes comprehensive error handling:

- Validates input parameters
- Handles network failures gracefully
- Logs errors without crashing the application
- Warns about missing configuration

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass
2. Code follows existing conventions
3. New features include tests
4. Documentation is updated

## License

MIT
