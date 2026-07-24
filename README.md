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

// Send alert for single opportunity
await service.sendBountyAlert(1);
// Output: 🎯 Bounty Alert: 1 New Opportunity found
```

### Batch Notifications

```javascript
const counts = [1, 5, 13];
const results = await service.sendBatchAlerts(counts);
```

### Custom Notification Options

```javascript
await service.sendBountyAlert(13, {
  priority: 'high',
  channel: 'slack',
  tags: ['urgent', 'high-value']
});
```

## Testing

```bash
npm test
```

## API Reference

### `formatBountyNotification(count)`

Formats a bounty notification message with proper pluralization.

- **Parameters:**
  - `count` (number): Number of opportunities found
- **Returns:** (string) Formatted notification message
- **Throws:** Error if count is invalid

### `NotificationService.sendBountyAlert(opportunityCount, options)`

Sends a bounty alert notification.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities
  - `options` (Object): Additional notification options
- **Returns:** Promise<Object> with success status and notification details

### `NotificationService.sendBatchAlerts(counts)`

Sends multiple bounty alerts in batch.

- **Parameters:**
  - `counts` (Array<number>): Array of opportunity counts
- **Returns:** Promise<Array<Object>> with results for each notification

## Fix Details

This fix addresses the typo in the notification message:
- ❌ Before: "13 New Opportunityies found" (incorrect pluralization)
- ✅ After: "13 New Opportunities found" (correct pluralization)

The implementation includes:
1. Proper singular/plural handling ("Opportunity" vs "Opportunities")
2. Comprehensive error handling for edge cases
3. Full test coverage
4. Service layer for notification management
5. Batch notification support

## License

MIT
