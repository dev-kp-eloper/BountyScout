# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notification system with proper pluralization
- 🔔 Customizable alert formatting
- ✅ Comprehensive error handling

## Installation

```bash
npm install
```

## Usage

### Formatting Bounty Alerts

```javascript
const { formatBountyAlert } = require('./src/utils/notificationFormatter');

// Single opportunity
console.log(formatBountyAlert(1));
// Output: 🎯 Bounty Alert: 1 New Opportunity found

// Multiple opportunities
console.log(formatBountyAlert(19));
// Output: 🎯 Bounty Alert: 19 New Opportunities found
```

### Sending Notifications

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');

// Send a bounty alert
const result = await sendBountyAlert(19, {
  channel: 'slack',
  priority: 'high'
});

console.log(result);
// Output: { success: true, message: '🎯 Bounty Alert: 19 New Opportunities found', ... }
```

## Testing

```bash
npm test
```

## API Reference

### `formatBountyAlert(count)`

Formats a bounty alert message with proper pluralization.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted alert message

**Throws:** Error if count is not a non-negative number

### `sendBountyAlert(opportunityCount, options)`

Sends a bounty alert notification.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities
- `options` (Object): Optional notification settings

**Returns:** (Promise<Object>) Notification result with success status

## Error Handling

The notification system includes comprehensive error handling:
- Validates input types and ranges
- Logs errors for debugging
- Returns structured error responses
- Prevents crashes from invalid data

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
