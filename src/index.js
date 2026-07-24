const { Octokit } = require('@octokit/rest');
const fs = require('fs').promises;
const path = require('path');
const { sendNotification } = require('./notifier');
const { filterBounties, deduplicateBounties } = require('./utils');

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const DATA_FILE = path.join(__dirname, '../data/bounties.json');

const octokit = new Octokit({
  auth: GITHUB_TOKEN
});

const BOUNTY_LABELS = [
  'bounty',
  'bug-bounty',
  'reward',
  'prize',
  'hackathon',
  'paid',
  'compensation',
  'bounty-hunter',
  'good-first-bounty'
];

const BOUNTY_KEYWORDS = [
  'bounty',
  'reward',
  'prize',
  '$',
  'USD',
  'EUR',
  'compensation',
  'paid issue'
];

async function loadExistingBounties() {
  try {
    const data = await fs.readFile(DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    if (error.code === 'ENOENT') {
      return { bounties: [], lastUpdated: null };
    }
    throw error;
  }
}

async function saveBounties(data) {
  try {
    await fs.mkdir(path.dirname(DATA_FILE), { recursive: true });
    await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error saving bounties:', error);
    throw error;
  }
}

async function searchBountiesByLabel(label) {
  try {
    const response = await octokit.search.issuesAndPullRequests({
      q: `label:${label} is:issue is:open`,
      sort: 'created',
      order: 'desc',
      per_page: 30
    });
    return response.data.items;
  } catch (error) {
    console.error(`Error searching for label ${label}:`, error.message);
    return [];
  }
}

async function searchBountiesByKeyword(keyword) {
  try {
    const response = await octokit.search.issuesAndPullRequests({
      q: `${keyword} in:title,body is:issue is:open`,
      sort: 'created',
      order: 'desc',
      per_page: 20
    });
    return response.data.items;
  } catch (error) {
    console.error(`Error searching for keyword ${keyword}:`, error.message);
    return [];
  }
}

function parseIssueData(issue) {
  return {
    id: issue.id,
    number: issue.number,
    title: issue.title,
    url: issue.html_url,
    repository: issue.repository_url.replace('https://api.github.com/repos/', ''),
    state: issue.state,
    labels: issue.labels.map(l => l.name),
    createdAt: issue.created_at,
    updatedAt: issue.updated_at,
    body: issue.body ? issue.body.substring(0, 500) : '',
    author: issue.user.login,
    comments: issue.comments
  };
}

async function findNewBounties() {
  console.log('🔍 Searching for bounty opportunities...');
  
  const allIssues = [];
  
  // Search by labels
  for (const label of BOUNTY_LABELS) {
    console.log(`Searching for label: ${label}`);
    const issues = await searchBountiesByLabel(label);
    allIssues.push(...issues);
    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Search by keywords
  for (const keyword of BOUNTY_KEYWORDS) {
    console.log(`Searching for keyword: ${keyword}`);
    const issues = await searchBountiesByKeyword(keyword);
    allIssues.push(...issues);
    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Parse and deduplicate
  const parsedIssues = allIssues.map(parseIssueData);
  const uniqueIssues = deduplicateBounties(parsedIssues);
  
  // Filter out non-bounty issues
  const filteredBounties = filterBounties(uniqueIssues);
  
  console.log(`Found ${filteredBounties.length} potential bounties`);
  
  return filteredBounties;
}

async function main() {
  try {
    console.log('🎯 Bounty Scout Starting...');
    
    // Load existing bounties
    const existingData = await loadExistingBounties();
    const existingIds = new Set(existingData.bounties.map(b => b.id));
    
    // Find new bounties
    const allBounties = await findNewBounties();
    
    // Identify new opportunities
    const newBounties = allBounties.filter(b => !existingIds.has(b.id));
    
    console.log(`📊 Found ${newBounties.length} new opportunities`);
    
    if (newBounties.length > 0) {
      // Update data file
      const updatedData = {
        bounties: allBounties,
        lastUpdated: new Date().toISOString(),
        stats: {
          total: allBounties.length,
          new: newBounties.length
        }
      };
      
      await saveBounties(updatedData);
      
      // Generate report
      await generateReport(newBounties, allBounties);
      
      // Send notification
      await sendNotification({
        title: `🎯 Bounty Alert: ${newBounties.length} New Opportunit${newBounties.length === 1 ? 'y' : 'ies'} Found`,
        bounties: newBounties.slice(0, 10),
        total: allBounties.length
      });
      
      console.log('✅ Bounty Scout completed successfully');
    } else {
      console.log('ℹ️ No new bounties found');
    }
    
  } catch (error) {
    console.error('❌ Error running Bounty Scout:', error);
    process.exit(1);
  }
}

async function generateReport(newBounties, allBounties) {
  const reportPath = path.join(__dirname, '../README.md');
  
  let report = `# 🎯 Bounty Scout\n\n`;
  report += `Automated bounty opportunity finder for GitHub issues.\n\n`;
  report += `**Last Updated:** ${new Date().toISOString()}\n\n`;
  report += `**Total Bounties:** ${allBounties.length}\n`;
  report += `**New Opportunities:** ${newBounties.length}\n\n`;
  
  if (newBounties.length > 0) {
    report += `## 🆕 Latest Opportunities\n\n`;
    
    for (const bounty of newBounties.slice(0, 20)) {
      report += `### [${bounty.title}](${bounty.url})\n`;
      report += `**Repository:** ${bounty.repository}\n`;
      report += `**Created:** ${new Date(bounty.createdAt).toLocaleDateString()}\n`;
      report += `**Labels:** ${bounty.labels.join(', ')}\n\n`;
      
      if (bounty.body) {
        const preview = bounty.body.substring(0, 200).replace(/\n/g, ' ');
        report += `${preview}...\n\n`;
      }
      
      report += `---\n\n`;
    }
  }
  
  report += `## 📊 All Active Bounties\n\n`;
  report += `| Repository | Title | Created | Labels |\n`;
  report += `|------------|-------|---------|--------|\n`;
  
  for (const bounty of allBounties.slice(0, 50)) {
    const repo = bounty.repository.split('/').pop();
    const title = bounty.title.substring(0, 50);
    const date = new Date(bounty.createdAt).toLocaleDateString();
    const labels = bounty.labels.slice(0, 3).join(', ');
    report += `| ${repo} | [${title}](${bounty.url}) | ${date} | ${labels} |\n`;
  }
  
  report += `\n## 🚀 Usage\n\n`;
  report += `This repository automatically scans GitHub for bounty opportunities every 6 hours.\n\n`;
  report += `### Running Locally\n\n`;
  report += `\`\`\`bash\n`;
  report += `npm install\n`;
  report += `export GITHUB_TOKEN=your_token_here\n`;
  report += `npm start\n`;
  report += `\`\`\`\n\n`;
  report += `## 📝 License\n\nMIT\n`;
  
  await fs.writeFile(reportPath, report);
  console.log('📄 Report generated');
}

if (require.main === module) {
  main();
}

module.exports = { findNewBounties, main };
