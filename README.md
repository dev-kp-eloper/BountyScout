# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Smart notifications with proper pluralization
- 🔍 Opportunity filtering and formatting
- ✅ Comprehensive error handling

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

// Send bounty alert
const opportunities = [
  { title: 'Bug Fix', reward: '$500', url: 'https://example.com/1' },
  { title: 'Feature Request', reward: '$1000', url: 'https://example.com/2' }
];

await notificationService.sendBountyAlert(opportunities.length, opportunities);

// Format notification message
const message = formatBountyNotification(13);
console.log(message); // "🎯 Bounty Alert: 13 New Opportunities found"
```

## Testing

```bash
npm test
```

## API

### `formatBountyNotification(count)`

Formats a bounty notification message with proper pluralization.

- **Parameters:**
  - `count` (number): Number of new opportunities
- **Returns:** Formatted notification string
- **Throws:** Error if count is invalid

### `NotificationService`

#### `sendBountyAlert(opportunityCount, opportunities)`

Sends a bounty alert notification.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities
  - `opportunities` (Array): Array of opportunity objects
- **Returns:** Promise resolving to notification result object

#### `formatOpportunityDetails(opportunities)`

Formats opportunity details for display.

- **Parameters:**
  - `opportunities` (Array): Array of opportunity objects
- **Returns:** Formatted string with opportunity details

## Fix Details

This fix addresses the typo in the notification message:
- ❌ Before: "13 New Opportunityies found" (typo)
- ✅ After: "13 New Opportunities found" (correct)

The implementation includes:
- Proper singular/plural handling ("Opportunity" vs "Opportunities")
- Comprehensive error handling
- Full test coverage
- Extensible notification service architecture

## License

MIT
