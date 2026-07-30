# BountyScout

Automated bounty opportunity scanner for GitHub issues.

## Features

- Scans GitHub repositories for bounty opportunities
- Automated issue creation for discovered bounties
- Configurable scanning intervals

## Configuration

### Self-Reference Protection

BountyScout automatically prevents recursive issue creation by:

1. **Auto-closing self-referencing alerts**: Issues that reference the BountyScout repository itself are automatically closed
2. **Exclusion list**: Add your repository to the scanner's exclusion list to prevent scanning

### Recommended Scanner Configuration

To prevent infinite loops, configure your bounty scanner to exclude:

```json
{
  "excluded_repos": [
    "vansh-09/BountyScout",
    "freedom-winds/BountyScout"
  ],
  "exclude_self": true
}
```

## Setup

1. Fork this repository
2. Configure GitHub Actions secrets
3. Enable issue creation in repository settings
4. The workflow will automatically close any self-referencing bounty alerts

## Issue Management

Bounty alert issues that reference this repository are automatically:
- Closed with `not_planned` status
- Tagged with an explanatory comment
- Prevented from triggering additional scans

## Contributing

Contributions welcome! Please ensure your scanner implementation:
- Excludes the repository running the scanner
- Validates bounty sources before creating issues
- Implements rate limiting to prevent spam

## License

MIT License - See LICENSE file for details
