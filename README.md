# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notification system with proper pluralization
- 🔔 Batch notification support
- ✅ Comprehensive error handling
- 🧪 Full test coverage

## Installation

```bash
npm install
```

## Usage

### Basic Notification

```javascript
const NotificationService = require('./src/services/notificationService');

const service = new NotificationService();

// Send a single bounty alert
await service.sendBountyAlert(13);
// Output: 🎯 Bounty Alert: 13 New Opportunities found

await service.sendBountyAlert(1);
// Output: 🎯 Bounty Alert: 1 New Opportunity found
```

### Batch Notifications

```javascript
const alerts = [
  { count: 13, options: { category: 'web3' } },
  { count: 5, options: { category: 'mobile' } },
  { count: 1, options: { category: 'backend' } }
];

const results = await service.sendBatchAlerts(alerts);
```

### Formatting Utility

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

### NotificationService

#### `sendBountyAlert(opportunityCount, options)`

Sends a bounty alert notification.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities found
  - `options` (Object, optional): Additional notification options
- **Returns:** Promise<Object> - Notification result

#### `sendBatchAlerts(alerts)`

Sends multiple bounty alerts in batch.

- **Parameters:**
  - `alerts` (Array<Object>): Array of alert objects
- **Returns:** Promise<Array<Object>> - Array of notification results

### formatBountyNotification(count)

Formats a bounty notification message with proper pluralization.

- **Parameters:**
  - `count` (number): Number of opportunities
- **Returns:** string - Formatted notification message
- **Throws:** Error if count is invalid

## Error Handling

The notification system includes comprehensive error handling:

- Validates input types and ranges
- Handles negative numbers gracefully
- Logs errors for debugging
- Returns structured error responses

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
