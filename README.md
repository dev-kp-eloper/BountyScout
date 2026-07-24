# BountyScout

A tool to scan and alert for new bounty opportunities.

## Features

- 🎯 Automated bounty opportunity scanning
- 📧 Smart notifications with proper spelling
- 🔍 Multi-platform support
- ✅ Comprehensive error handling

## Installation

```bash
npm install
```

## Usage

```javascript
const BountyScanner = require('./src/scanner/bountyScanner');
const NotificationService = require('./src/notifications/notificationService');

// Create scanner instance
const scanner = new BountyScanner();

// Scan for opportunities
await scanner.scan();

// Send custom notification
await NotificationService.sendBountyAlert(13, opportunities);
```

## Testing

```bash
npm test
```

## Recent Fixes

### Spelling Correction
- Fixed typo: "Opportunityies" → "Opportunities"
- Added spell-check utility for common typos
- Implemented automatic correction in notification titles

## License

MIT
