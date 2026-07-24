# BountyScout 🎯

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🔍 Scout for new bounty opportunities
- 🔔 Get notified when new opportunities are found
- 📊 Track bounty statistics
- ✅ Proper pluralization in notifications

## Installation

```bash
npm install
```

## Usage

### Basic Example

```javascript
const NotificationService = require('./src/services/notificationService');
const { formatBountyAlert } = require('./src/utils/notificationFormatter');

// Create notification service
const notificationService = new NotificationService();

// Subscribe to notifications
notificationService.subscribe((notification) => {
  console.log(notification.message);
  console.log(`Found ${notification.count} opportunities`);
});

// Send alert
const opportunities = [
  { id: 1, title: 'Fix typo in documentation', reward: 50 },
  { id: 2, title: 'Add new feature', reward: 500 }
];

notificationService.sendBountyAlert(opportunities.length, opportunities);
// Output: 🎯 Bounty Alert: 2 New Opportunities found
```

### Format Messages

```javascript
const { formatBountyAlert } = require('./src/utils/notificationFormatter');

console.log(formatBountyAlert(1));  // 🎯 Bounty Alert: 1 New Opportunity found
console.log(formatBountyAlert(13)); // 🎯 Bounty Alert: 13 New Opportunities found
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlert(count)`

Formats a bounty alert message with proper pluralization.

**Parameters:**
- `count` (number): Number of new opportunities

**Returns:** Formatted string message

**Throws:** Error if count is not a non-negative number

### `NotificationService`

#### `subscribe(callback)`

Subscribe to bounty notifications.

**Parameters:**
- `callback` (Function): Function to call when notifications are sent

#### `unsubscribe(callback)`

Unsubscribe from bounty notifications.

**Parameters:**
- `callback` (Function): Function to remove from subscribers

#### `sendBountyAlert(count, opportunities)`

Send a bounty alert notification to all subscribers.

**Parameters:**
- `count` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects (optional)

**Returns:** Notification object

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
