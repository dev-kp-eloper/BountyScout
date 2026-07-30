# BountyScout

Automated GitHub bounty and opportunity scanner.

## Features

- Automated scanning for bounty opportunities across GitHub
- Duplicate alert detection and cleanup
- Structured issue templates for consistent reporting

## Automated Workflows

### Bounty Alert Deduplication

The repository automatically manages bounty alert issues:

- **Trigger**: Runs every 6 hours and when new bounty alerts are created
- **Action**: Keeps only the most recent bounty alert open, closes older duplicates
- **Labels**: Uses `bounty-scan` label for tracking

### Alert Validation

Validates bounty alert format on creation:

- Checks for required scan timestamp
- Verifies opportunity list is present
- Flags malformed alerts for review

## Issue Templates

Use the **Bounty Alert** template when creating scan result issues. The template ensures:

- Consistent formatting
- Automatic labeling
- Proper metadata tracking

## Contributing

Contributions welcome! Please:

1. Use the provided issue templates
2. Follow existing code style
3. Test workflows locally when possible

## License

MIT
