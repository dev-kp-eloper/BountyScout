const { Octokit } = require('@octokit/rest');
const fs = require('fs');
const path = require('path');

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_KEYWORDS = [
  'bounty',
  'reward',
  'prize',
  'hackathon',
  'gitcoin',
  'bountysource'
];

const BOUNTY_LABELS = [
  'bounty',
  'bounties',
  'reward',
  'prize',
  'gitcoin',
  'hacktoberfest'
];

const CACHE_FILE = path.join(__dirname, '..', 'cache.json');
const RESULTS_FILE = path.join(__dirname, '..', 'results.json');

function loadCache() {
  try {
    if (fs.existsSync(CACHE_FILE)) {
      const data = fs.readFileSync(CACHE_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Error loading cache:', error.message);
  }
  return { scannedIssues: [] };
}

function saveCache(cache) {
  try {
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
  } catch (error) {
    console.error('Error saving cache:', error.message);
  }
}

function saveResults(results) {
  try {
    fs.writeFileSync(RESULTS_FILE, JSON.stringify(results, null, 2));
  } catch (error) {
    console.error('Error saving results:', error.message);
  }
}

function isBountyIssue(issue) {
  const title = (issue.title || '').toLowerCase();
  const body = (issue.body || '').toLowerCase();
  const labels = (issue.labels || []).map(l => (typeof l === 'string' ? l : l.name).toLowerCase());
  
  // Check labels first
  if (labels.some(label => BOUNTY_LABELS.includes(label))) {
    return true;
  }
  
  // Check title and body for keywords
  const text = `${title} ${body}`;
  return BOUNTY_KEYWORDS.some(keyword => text.includes(keyword));
}

function extractReward(issue) {
  const text = `${issue.title || ''} ${issue.body || ''}`;
  
  // Common reward patterns
  const patterns = [
    /\$([0-9,]+(?:\.[0-9]{2})?)/,
    /([0-9,]+)\s*(?:USD|usd|dollars?)/i,
    /reward[:\s]+([^\n]+)/i,
    /bounty[:\s]+([^\n]+)/i
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1].trim();
    }
  }
  
  return null;
}

async function searchBountyIssues() {
  const newBounties = [];
  const cache = loadCache();
  const scannedIssues = new Set(cache.scannedIssues || []);
  
  try {
    console.log('Searching for bounty issues...');
    
    // Search for issues with bounty-related labels
    for (const label of BOUNTY_LABELS) {
      try {
        const { data } = await octokit.search.issuesAndPullRequests({
          q: `label:${label} is:issue is:open`,
          sort: 'created',
          order: 'desc',
          per_page: 30
        });
        
        console.log(`Found ${data.items.length} issues with label "${label}"`);
        
        for (const issue of data.items) {
          const issueId = `${issue.repository_url}#${issue.number}`;
          
          if (scannedIssues.has(issueId)) {
            continue;
          }
          
          if (isBountyIssue(issue)) {
            const repoUrl = issue.repository_url.replace('https://api.github.com/repos/', 'https://github.com/');
            const repoName = issue.repository_url.replace('https://api.github.com/repos/', '');
            
            newBounties.push({
              title: issue.title,
              repo: repoName,
              repoUrl: repoUrl,
              issueNumber: issue.number,
              issueUrl: issue.html_url,
              reward: extractReward(issue),
              labels: issue.labels.map(l => typeof l === 'string' ? l : l.name),
              language: null,
              createdAt: issue.created_at
            });
            
            scannedIssues.add(issueId);
          }
        }
        
        // Rate limiting
        await new Promise(resolve => setTimeout(resolve, 2000));
      } catch (error) {
        console.error(`Error searching for label "${label}":`, error.message);
      }
    }
    
    // Search for issues with bounty keywords in title
    for (const keyword of BOUNTY_KEYWORDS) {
      try {
        const { data } = await octokit.search.issuesAndPullRequests({
          q: `${keyword} in:title is:issue is:open`,
          sort: 'created',
          order: 'desc',
          per_page: 20
        });
        
        console.log(`Found ${data.items.length} issues with keyword "${keyword}" in title`);
        
        for (const issue of data.items) {
          const issueId = `${issue.repository_url}#${issue.number}`;
          
          if (scannedIssues.has(issueId)) {
            continue;
          }
          
          if (isBountyIssue(issue)) {
            const repoUrl = issue.repository_url.replace('https://api.github.com/repos/', 'https://github.com/');
            const repoName = issue.repository_url.replace('https://api.github.com/repos/', '');
            
            newBounties.push({
              title: issue.title,
              repo: repoName,
              repoUrl: repoUrl,
              issueNumber: issue.number,
              issueUrl: issue.html_url,
              reward: extractReward(issue),
              labels: issue.labels.map(l => typeof l === 'string' ? l : l.name),
              language: null,
              createdAt: issue.created_at
            });
            
            scannedIssues.add(issueId);
          }
        }
        
        // Rate limiting
        await new Promise(resolve => setTimeout(resolve, 2000));
      } catch (error) {
        console.error(`Error searching for keyword "${keyword}":`, error.message);
      }
    }
    
    // Remove duplicates based on issue URL
    const uniqueBounties = [];
    const seenUrls = new Set();
    
    for (const bounty of newBounties) {
      if (!seenUrls.has(bounty.issueUrl)) {
        seenUrls.add(bounty.issueUrl);
        uniqueBounties.push(bounty);
      }
    }
    
    console.log(`\nFound ${uniqueBounties.length} new unique bounty opportunities`);
    
    // Save cache and results
    cache.scannedIssues = Array.from(scannedIssues);
    cache.lastScanned = new Date().toISOString();
    saveCache(cache);
    
    const results = {
      newBounties: uniqueBounties,
      scannedAt: new Date().toISOString(),
      totalScanned: scannedIssues.size
    };
    saveResults(results);
    
    return uniqueBounties;
  } catch (error) {
    console.error('Error searching for bounties:', error);
    throw error;
  }
}

// Run the scout
searchBountyIssues()
  .then(bounties => {
    console.log('\nBounty scout completed successfully!');
    process.exit(0);
  })
  .catch(error => {
    console.error('\nBounty scout failed:', error);
    process.exit(1);
  });