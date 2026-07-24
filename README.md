# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notification system with proper pluralization
- 🔍 Comprehensive opportunity filtering
- ✅ Full test coverage

## Installation

```bash
npm install
```

## Usage

### Notification Service

```javascript
const NotificationService = require('./src/services/notificationService');

const service = new NotificationService();

// Send a single alert
const opportunities = [
  { title: 'Bug Fix', reward: '$500' },
  { title: 'Feature Request', reward: '$1000' }
];

await service.sendBountyAlert(2, opportunities);
// Output: 🎯 Bounty Alert: 2 New Opportunities found

// Send bulk alerts
const alerts = [
  { count: 13, opportunities: [...] },
  { count: 1, opportunities: [...] }
];

await service.sendBulkAlerts(alerts);
```

### Notification Formatter

```javascript
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

formatBountyNotification(1);  // "🎯 Bounty Alert: 1 New Opportunity found"
formatBountyNotification(13); // "🎯 Bounty Alert: 13 New Opportunities found"
formatBountyNotification(0);  // "🎯 Bounty Alert: No new opportunities found"
```

## Testing

```bash
npm test
```

## Fix Details

This fix addresses the typo in bounty notifications:
- ❌ Before: "13 New Opportunityies found" (incorrect pluralization)
- ✅ After: "13 New Opportunities found" (correct pluralization)

The implementation includes:
- Proper singular/plural handling ("Opportunity" vs "Opportunities")
- Comprehensive error handling
- Full test coverage
- Production-ready notification service

## License

MIT
