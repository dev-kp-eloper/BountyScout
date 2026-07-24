# BountyScout

A tool for tracking and alerting on new bounty opportunities.

## Features

- 🎯 Real-time bounty alerts
- 📊 Opportunity tracking
- 🔔 Notification system
- ✨ Automatic typo correction

## Installation

```bash
npm install
```

## Usage

### Sending Bounty Alerts

```javascript
const NotificationService = require('./src/notifications/notificationService');

// Send an alert for new opportunities
await NotificationService.sendBountyAlert(13);
// Output: 🎯 Bounty Alert: 13 New Opportunities found
```

### Fixing Typos

The project includes automatic typo correction for common mistakes:

```javascript
const { fixTypos } = require('./src/utils/textFormatter');

const message = '13 New Opportunityies found';
const fixed = fixTypos(message);
// Output: '13 New Opportunities found'
```

### Running the Typo Fix Script

To automatically fix typos across the entire project:

```bash
node scripts/fixNotificationTypos.js
```

## Testing

```bash
npm test
```

## API

### NotificationService

#### `generateBountyAlert(count)`

Generates a properly formatted bounty alert message.

- **Parameters:**
  - `count` (number): Number of opportunities found
- **Returns:** (string) Formatted alert message

#### `sendBountyAlert(count, options)`

Sends a bounty alert notification.

- **Parameters:**
  - `count` (number): Number of opportunities found
  - `options` (Object): Additional options (optional)
- **Returns:** (Promise<Object>) Notification result

#### `fixNotificationMessage(message)`

Fixes typos in notification messages.

- **Parameters:**
  - `message` (string): Message to fix
- **Returns:** (string) Corrected message

### Text Formatter

#### `fixTypos(text)`

Fixes common typos in text.

- **Parameters:**
  - `text` (string): Text to fix
- **Returns:** (string) Corrected text

#### `pluralize(word, count)`

Correctly pluralizes a word based on count.

- **Parameters:**
  - `word` (string): Word to pluralize
  - `count` (number): Count to determine pluralization
- **Returns:** (string) Correctly pluralized word

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
