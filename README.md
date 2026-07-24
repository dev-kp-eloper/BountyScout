# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Multi-channel notifications (Console, Email, Slack)
- ✅ Proper pluralization in notifications
- 🧪 Comprehensive test coverage

## Installation

```bash
npm install
```

## Usage

### Basic Notification

```javascript
const NotificationService = require('./src/services/notificationService');

const service = new NotificationService();

// Send a bounty alert
await service.sendBountyAlert(13);
// Output: 🎯 Bounty Alert: 13 New Opportunities found

await service.sendBountyAlert(1);
// Output: 🎯 Bounty Alert: 1 New Opportunity found
```

### Multi-Channel Notifications

```javascript
// Send to multiple channels
await service.sendMultiChannelAlert(13, ['console', 'email', 'slack']);
```

### Using the Formatter Directly

```javascript
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

const message = formatBountyNotification(13);
console.log(message);
// Output: 🎯 Bounty Alert: 13 New Opportunities found
```

## Testing

```bash
npm test
```

## API Reference

### `formatBountyNotification(count)`

Formats a bounty notification message with proper pluralization.

- **Parameters:**
  - `count` (number): Number of new opportunities
- **Returns:** (string) Formatted notification message
- **Throws:** Error if count is not a non-negative number

### `NotificationService.sendBountyAlert(opportunityCount, options)`

Sends a bounty alert notification.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities found
  - `options` (Object): Additional notification options
- **Returns:** Promise<Object> Notification result

### `NotificationService.sendMultiChannelAlert(opportunityCount, channels)`

Sends notifications through multiple channels.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities
  - `channels` (Array<string>): Notification channels
- **Returns:** Promise<Object> Results from all channels

## Fix Details

This fix addresses the typo in the notification message:
- ❌ Before: "13 New Opportunityies found" (incorrect pluralization)
- ✅ After: "13 New Opportunities found" (correct pluralization)

The implementation includes:
1. Proper pluralization logic ("Opportunity" vs "Opportunities")
2. Error handling for invalid inputs
3. Comprehensive test coverage
4. Multi-channel notification support
5. Extensible architecture for future enhancements

## License

MIT
