# BountyScout

A tool to scout and notify about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Smart notifications with proper grammar
- 🔍 Multi-platform support
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
  { title: 'Bug Fix', reward: '$500', platform: 'GitHub' },
  { title: 'Feature Request', reward: '$1000', platform: 'GitLab' }
];

await notificationService.sendBountyAlert(opportunities.length, opportunities);

// Format notification message
const message = formatBountyNotification(19); // "🎯 Bounty Alert: 19 New Opportunities found"
```

## Testing

```bash
npm test
```

## API

### `formatBountyNotification(count)`

Formats a bounty notification message with proper singular/plural grammar.

- **Parameters:**
  - `count` (number): Number of new opportunities
- **Returns:** (string) Formatted notification message
- **Throws:** Error if count is invalid

### `NotificationService`

#### `sendBountyAlert(opportunityCount, opportunities)`

Sends a bounty alert notification.

- **Parameters:**
  - `opportunityCount` (number): Number of new opportunities
  - `opportunities` (Array): Array of opportunity objects
- **Returns:** Promise<Object> with success status and notification details

#### `formatOpportunityDetails(opportunity)`

Formats opportunity details for display.

- **Parameters:**
  - `opportunity` (Object): Opportunity object with title, reward, and platform
- **Returns:** (string) Formatted opportunity string

## Fix Details

This fix addresses the typo in bounty notifications:
- ❌ Before: "19 New Opportunityies found" (incorrect spelling)
- ✅ After: "19 New Opportunities found" (correct spelling)

The implementation includes:
- Proper singular/plural handling ("Opportunity" vs "Opportunities")
- Input validation and error handling
- Comprehensive test coverage
- Extensible notification service

## License

MIT
