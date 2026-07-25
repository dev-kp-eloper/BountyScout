# 🎯 BountyScout

Automated bounty opportunity finder that scouts for bug bounties and security rewards across GitHub and other platforms.

## Features

- 🔍 Automatically searches for new bounty opportunities
- 🤖 Creates GitHub issues for new findings
- 📊 Tracks bounties to avoid duplicates
- ⏰ Runs on a schedule via GitHub Actions
- 🎯 Searches multiple sources (GitHub issues, repositories, platforms)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dev-kp-eloper/BountyScout.git
   cd BountyScout
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your GitHub token:
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_REPOSITORY=dev-kp-eloper/BountyScout
   ```

4. **Run locally**
   ```bash
   npm start
   ```

## GitHub Actions Setup

The workflow is automatically configured to run every 6 hours. Make sure you have:

1. Enabled GitHub Actions in your repository
2. The `GITHUB_TOKEN` is automatically provided by GitHub Actions
3. Repository permissions set to allow issue creation

## How It Works

1. **Scout Phase**: Searches for bounties across multiple sources
   - GitHub issues with bounty labels
   - Repositories with bug bounty programs
   - Security.txt files

2. **Detection Phase**: Compares new findings with previous data
   - Identifies truly new opportunities
   - Filters out duplicates

3. **Notification Phase**: Creates a GitHub issue with all new bounties
   - Fixed typo: "Opportunities" instead of "Opportunityies"
   - Formatted list with links and details
   - Automatic labeling

## Project Structure

```
BountyScout/
├── .github/
│   └── workflows/
│       └── bounty-scout.yml    # GitHub Actions workflow
├── src/
│   ├── index.js                # Main scout logic
│   └── create-issue.js         # Issue creation logic
├── data/                       # Bounty database (gitignored)
├── package.json
├── .env.example
├── .gitignore
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own bounty hunting!

## Disclaimer

This tool is for informational purposes only. Always verify bounty programs and follow responsible disclosure practices.
