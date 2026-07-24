# BountyScout 🎯

A tool to scout and track bug bounty opportunities across multiple platforms.

## Features

- 🔍 Automated bounty opportunity discovery
- 📢 Smart notification system with proper pluralization
- 🎯 Multi-platform support
- 📊 Opportunity tracking and management

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
  { title: 'XSS Vulnerability', reward: '$500', platform: 'HackerOne' },
  { title: 'SQL Injection', reward: '$1000', platform: 'Bugcrowd' }
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

### NotificationService

#### `sendBountyAlert(count, opportunities)`

Sends a bounty alert notification.

- `count` (number): Number of new opportunities found
- `opportunities` (Array): Array of opportunity objects
- Returns: Promise<Object> - Notification result

#### `formatOpportunityList(opportunities)`

Formats opportunity details for display.

- `opportunities` (Array): Array of opportunity objects
- Returns: string - Formatted opportunity list

### Utility Functions

#### `formatBountyNotification(count)`

Formats notification messages with proper pluralization.

- `count` (number): Number of opportunities
- Returns: string - Formatted notification message

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
