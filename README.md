# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Customizable notification system
- 🔍 Smart filtering and search
- 📊 Analytics and reporting

## Installation

```bash
npm install
```

## Usage

```javascript
const NotificationService = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Create notification service
const notificationService = new NotificationService();

// Register a notification handler
notificationService.registerHandler((data) => {
  console.log(data.message);
  console.log(`Found ${data.count} opportunities`);
});

// Send bounty alert
await notificationService.sendBountyAlert(13, opportunities);
```

## Notification Format

Notifications are automatically formatted with proper grammar:
- Single opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 13 New Opportunities found"
- No opportunities: "🎯 Bounty Alert: No new opportunities found"

## Testing

```bash
npm test
```

## API

### NotificationService

#### `registerHandler(handler)`
Register a function to handle notifications.

#### `sendBountyAlert(count, opportunities)`
Send a bounty alert notification with the specified count and opportunity data.

#### `clearHandlers()`
Remove all registered notification handlers.

### formatBountyNotification(count)

Formats a bounty notification message with proper grammar.

**Parameters:**
- `count` (number): Number of new opportunities

**Returns:** Formatted notification string

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
