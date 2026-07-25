const { Octokit } = require('@octokit/rest');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const DATA_FILE = path.join(__dirname, '..', 'data', 'bounties.json');
const BOUNTY_KEYWORDS = ['bounty', 'reward', '$', '💰', '🎯', 'prize', 'compensation'];

// Ensure data directory exists
function ensureDataDirectory() {
  const dataDir = path.join(__dirname, '..', 'data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
}

// Load existing bounties
function loadExistingBounties() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const data = fs.readFileSync(DATA_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Error loading existing bounties:', error.message);
  }
  return { bounties: [], lastChecked: null };
}

// Save bounties to file
function saveBounties(data) {
  try {
    ensureDataDirectory();
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error saving bounties:', error.message);
  }
}

// Check if text contains bounty keywords
function containsBountyKeywords(text) {
  if (!text) return false;
  const lowerText = text.toLowerCase();
  return BOUNTY_KEYWORDS.some(keyword => lowerText.includes(keyword.toLowerCase()));
}

// Search for bounty issues across GitHub
async function searchBountyIssues() {
  const newBounties = [];
  const existingData = loadExistingBounties();
  const existingIds = new Set(existingData.bounties.map(b => b.id));

  try {
    // Search for issues with bounty-related keywords
    const searchQueries = [
      'bounty in:title,body is:issue is:open',
      'reward in:title,body is:issue is:open',
      '💰 in:title,body is:issue is:open',
      '🎯 in:title,body is:issue is:open'
    ];

    for (const query of searchQueries) {
      try {
        const response = await octokit.search.issuesAndPullRequests({
          q: query,
          sort: 'created',
          order: 'desc',
          per_page: 30
        });

        for (const issue of response.data.items) {
          // Skip pull requests
          if (issue.pull_request) continue;

          // Skip if already tracked
          if (existingIds.has(issue.id)) continue;

          // Verify it's actually a bounty
          if (containsBountyKeywords(issue.title) || containsBountyKeywords(issue.body)) {
            const bounty = {
              id: issue.id,
              title: issue.title,
              url: issue.html_url,
              repository: issue.repository_url.replace('https://api.github.com/repos/', ''),
              state: issue.state,
              created_at: issue.created_at,
              labels: issue.labels.map(l => l.name),
              found_at: new Date().toISOString()
            };

            newBounties.push(bounty);
            existingIds.add(issue.id);
          }
        }

        // Rate limiting - wait between queries
        await new Promise(resolve => setTimeout(resolve, 2000));
      } catch (error) {
        console.error(`Error searching with query "${query}":`, error.message);
      }
    }

    // Update and save data
    const updatedData = {
      bounties: [...existingData.bounties, ...newBounties],
      lastChecked: new Date().toISOString(),
      newCount: newBounties.length
    };

    saveBounties(updatedData);

    console.log(`Found ${newBounties.length} new bounty opportunities`);
    console.log(`Total tracked bounties: ${updatedData.bounties.length}`);

    return newBounties;
  } catch (error) {
    console.error('Error in searchBountyIssues:', error.message);
    throw error;
  }
}

// Main execution
async function main() {
  try {
    console.log('Starting Bounty Scout...');
    const newBounties = await searchBountyIssues();
    
    if (newBounties.length > 0) {
      console.log('\nNew Bounties Found:');
      newBounties.forEach((bounty, index) => {
        console.log(`${index + 1}. ${bounty.title}`);
        console.log(`   Repository: ${bounty.repository}`);
        console.log(`   URL: ${bounty.url}`);
        console.log('');
      });
    } else {
      console.log('No new bounties found.');
    }

    process.exit(0);
  } catch (error) {
    console.error('Fatal error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { searchBountyIssues, loadExistingBounties, containsBountyKeywords };