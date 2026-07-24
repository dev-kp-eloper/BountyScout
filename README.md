# BountyScout

A tool for tracking and notifying about new bug bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Smart notifications with proper pluralization
- 🔍 Multi-platform support (HackerOne, Bugcrowd, YesWeHack, etc.)
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
  { title: 'XSS Vulnerability', reward: 500, platform: 'HackerOne' },
  { title: 'SQL Injection', reward: 1000, platform: 'Bugcrowd' }
];

await notificationService.sendBountyAlert(13, opportunities);

// Format notification message
const message = formatBountyNotification(13);
console.log(message); // "🎯 Bounty Alert: 13 New Opportunities found"
```

## Testing

```bash
npm test
```

## API

### NotificationService

#### `sendBountyAlert(opportunityCount, opportunities)`

Sends a bounty alert notification.

- `opportunityCount` (number): Number of new opportunities found
- `opportunities` (Array): Array of opportunity objects
- Returns: Promise<Object> with success status and notification details

#### `formatOpportunityDetails(opportunity)`

Formats a single opportunity for display.

- `opportunity` (Object): Opportunity object with title, reward, and platform
- Returns: String with formatted opportunity details

### Utility Functions

#### `formatBountyNotification(count)`

Formats a bounty notification message with proper pluralization.

- `count` (number): Number of opportunities
- Returns: String with formatted notification message

## Bug Fixes

### Fixed: Typo in notification message

**Issue:** The notification message contained a typo: "Opportunityies" instead of "Opportunities"

**Solution:** 
- Implemented proper pluralization logic
- Added comprehensive test coverage
- Created reusable notification formatting utilities
- Added error handling for edge cases

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
