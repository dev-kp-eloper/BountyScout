# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notification system with proper pluralization
- 🔔 Multi-channel notification support
- ✅ Comprehensive error handling

## Installation

```bash
npm install
```

## Usage

### Formatting Notifications

```javascript
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

const message = formatBountyNotification(19);
console.log(message); // 🎯 Bounty Alert: 19 New Opportunities found
```

### Sending Notifications

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');

// Simple notification
await sendBountyNotification(19);

// With custom channels
await sendBountyNotification(19, {
  channels: [slackChannel, emailChannel]
});
```

## Testing

```bash
npm test
```

## API

### `formatBountyNotification(count)`

Formats a bounty notification message with proper pluralization.

- **Parameters:**
  - `count` (number): Number of opportunities found
- **Returns:** (string) Formatted notification message
- **Throws:** Error if count is not a non-negative number

### `sendBountyNotification(opportunityCount, options)`

Sends a bounty notification through configured channels.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities
  - `options` (Object): Optional configuration
    - `channels` (Array): Array of notification channel objects
- **Returns:** Promise resolving to result object with `success` and `message` or `error`

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
