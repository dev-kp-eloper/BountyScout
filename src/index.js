const { Octokit } = require('@octokit/rest');
const fs = require('fs').promises;
const path = require('path');

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_PLATFORMS = [
  { name: 'Gitcoin', searchQuery: 'bounty gitcoin' },
  { name: 'Bountysource', searchQuery: 'bounty bountysource' },
  { name: 'IssueHunt', searchQuery: 'bounty issuehunt' },
  { name: 'Open Collective', searchQuery: 'bounty "open collective"' },
  { name: 'General', searchQuery: 'label:bounty OR label:"bug bounty" OR label:"bounty program"' }
];

const BOUNTY_LABELS = [
  'bounty',
  'bug-bounty',
  'bounty-program',
  'reward',
  'prize',
  'gitcoin',
  'bountysource',
  'issuehunt'
];

const DATA_DIR = path.join(__dirname, '..', 'data');
const BOUNTIES_FILE = path.join(DATA_DIR, 'bounties.json');
const LAST_RUN_FILE = path.join(DATA_DIR, 'last_run.json');

async function ensureDataDirectory() {
  try {
    await fs.mkdir(DATA_DIR, { recursive: true });
  } catch (error) {
    console.error('Error creating data directory:', error.message);
  }
}

async function loadExistingBounties() {
  try {
    const data = await fs.readFile(BOUNTIES_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return { bounties: [], lastUpdated: null };
  }
}

async function loadLastRun() {
  try {
    const data = await fs.readFile(LAST_RUN_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return { lastRun: null, lastIssueId: null };
  }
}

async function saveBounties(bounties) {
  await fs.writeFile(
    BOUNTIES_FILE,
    JSON.stringify(bounties, null, 2),
    'utf8'
  );
}

async function saveLastRun(data) {
  await fs.writeFile(
    LAST_RUN_FILE,
    JSON.stringify(data, null, 2),
    'utf8'
  );
}

async function searchBountyIssues() {
  const allIssues = [];
  const seenUrls = new Set();
  
  // Search by labels
  for (const label of BOUNTY_LABELS) {
    try {
      const query = `label:"${label}" is:issue is:open`;
      console.log(`Searching for: ${query}`);
      
      const response = await octokit.search.issuesAndPullRequests({
        q: query,
        sort: 'created',
        order: 'desc',
        per_page: 30
      });
      
      for (const issue of response.data.items) {
        if (!issue.pull_request && !seenUrls.has(issue.html_url)) {
          seenUrls.add(issue.html_url);
          allIssues.push(issue);
        }
      }
      
      // Rate limiting
      await sleep(2000);
    } catch (error) {
      console.error(`Error searching for label "${label}":`, error.message);
    }
  }
  
  // Search by keywords in title/body
  const keywords = ['bounty', '$', 'reward', 'prize'];
  for (const keyword of keywords) {
    try {
      const query = `"${keyword}" in:title,body is:issue is:open`;
      console.log(`Searching for keyword: ${keyword}`);
      
      const response = await octokit.search.issuesAndPullRequests({
        q: query,
        sort: 'created',
        order: 'desc',
        per_page: 30
      });
      
      for (const issue of response.data.items) {
        if (!issue.pull_request && !seenUrls.has(issue.html_url) && isBountyRelated(issue)) {
          seenUrls.add(issue.html_url);
          allIssues.push(issue);
        }
      }
      
      await sleep(2000);
    } catch (error) {
      console.error(`Error searching for keyword "${keyword}":`, error.message);
    }
  }
  
  return allIssues;
}

function isBountyRelated(issue) {
  const text = `${issue.title} ${issue.body || ''}`.toLowerCase();
  const bountyKeywords = [
    'bounty',
    'reward',
    'prize',
    'gitcoin',
    'bountysource',
    'issuehunt',
    '$',
    'usd',
    'payment',
    'compensation'
  ];
  
  return bountyKeywords.some(keyword => text.includes(keyword));
}

function extractBountyAmount(issue) {
  const text = `${issue.title} ${issue.body || ''}`;
  
  // Match currency patterns
  const patterns = [
    /\$([0-9,]+(?:\.[0-9]{2})?)/g,
    /([0-9,]+(?:\.[0-9]{2})?)\s*(?:USD|usd)/g,
    /([0-9,]+)\s*(?:ETH|eth)/g,
    /([0-9,]+)\s*(?:DAI|dai)/g
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[0];
    }
  }
  
  return 'Amount not specified';
}

function parseBountyIssue(issue) {
  return {
    id: issue.id,
    title: issue.title,
    url: issue.html_url,
    repository: issue.repository_url.replace('https://api.github.com/repos/', ''),
    author: issue.user.login,
    createdAt: issue.created_at,
    updatedAt: issue.updated_at,
    state: issue.state,
    labels: issue.labels.map(l => l.name),
    amount: extractBountyAmount(issue),
    body: issue.body ? issue.body.substring(0, 500) : '',
    comments: issue.comments
  };
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function createIssueNotification(newBounties) {
  if (newBounties.length === 0) {
    console.log('No new bounties found');
    return;
  }
  
  const owner = process.env.GITHUB_REPOSITORY?.split('/')[0] || 'dev-kp-eloper';
  const repo = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'BountyScout';
  
  const title = `🎯 Bounty Alert: ${newBounties.length} New Opportunit${newBounties.length === 1 ? 'y' : 'ies'} Found`;
  
  let body = `## 🎯 New Bounty Opportunities\n\n`;
  body += `Found **${newBounties.length}** new bounty opportunit${newBounties.length === 1 ? 'y' : 'ies'}!\n\n`;
  body += `---\n\n`;
  
  for (const bounty of newBounties.slice(0, 20)) {
    body += `### [${bounty.title}](${bounty.url})\n\n`;
    body += `- **Repository:** ${bounty.repository}\n`;
    body += `- **Amount:** ${bounty.amount}\n`;
    body += `- **Created:** ${new Date(bounty.createdAt).toLocaleDateString()}\n`;
    body += `- **Labels:** ${bounty.labels.join(', ') || 'None'}\n`;
    body += `\n---\n\n`;
  }
  
  if (newBounties.length > 20) {
    body += `\n_... and ${newBounties.length - 20} more! Check the [bounties.json](./data/bounties.json) file for the complete list._\n`;
  }
  
  body += `\n\n**Last Updated:** ${new Date().toISOString()}\n`;
  body += `\n_This issue was automatically generated by BountyScout._`;
  
  try {
    await octokit.issues.create({
      owner,
      repo,
      title,
      body,
      labels: ['bounty-alert', 'automated']
    });
    console.log(`Created issue: ${title}`);
  } catch (error) {
    console.error('Error creating issue:', error.message);
  }
}

async function main() {
  try {
    console.log('Starting BountyScout...');
    
    await ensureDataDirectory();
    
    const existingData = await loadExistingBounties();
    const lastRun = await loadLastRun();
    
    const existingIds = new Set(existingData.bounties.map(b => b.id));
    
    console.log('Searching for bounty issues...');
    const issues = await searchBountyIssues();
    
    console.log(`Found ${issues.length} total bounty issues`);
    
    const parsedBounties = issues.map(parseBountyIssue);
    const newBounties = parsedBounties.filter(b => !existingIds.has(b.id));
    
    console.log(`Found ${newBounties.length} new bounties`);
    
    // Merge and deduplicate
    const allBounties = [...existingData.bounties, ...newBounties];
    const uniqueBounties = Array.from(
      new Map(allBounties.map(b => [b.id, b])).values()
    );
    
    // Sort by creation date (newest first)
    uniqueBounties.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    const bountyData = {
      bounties: uniqueBounties,
      lastUpdated: new Date().toISOString(),
      totalCount: uniqueBounties.length,
      newCount: newBounties.length
    };
    
    await saveBounties(bountyData);
    
    const lastRunData = {
      lastRun: new Date().toISOString(),
      lastIssueId: uniqueBounties[0]?.id || null,
      bountiesFound: newBounties.length
    };
    
    await saveLastRun(lastRunData);
    
    // Create GitHub issue if new bounties found
    if (newBounties.length > 0) {
      await createIssueNotification(newBounties);
    }
    
    console.log('BountyScout completed successfully!');
    console.log(`Total bounties tracked: ${uniqueBounties.length}`);
    console.log(`New bounties found: ${newBounties.length}`);
    
  } catch (error) {
    console.error('Error in main execution:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main, searchBountyIssues, parseBountyIssue };
