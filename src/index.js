const { Octokit } = require('@octokit/rest');
const fs = require('fs').promises;
const path = require('path');

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_PLATFORMS = [
  { name: 'Gitcoin', query: 'gitcoin bounty in:title,body is:issue is:open' },
  { name: 'Bountysource', query: 'bountysource in:title,body is:issue is:open' },
  { name: 'IssueHunt', query: 'issuehunt in:title,body is:issue is:open' },
  { name: 'Algora', query: 'algora bounty in:title,body is:issue is:open' },
  { name: 'Generic', query: 'bounty OR reward OR prize in:title is:issue is:open label:bounty' }
];

const EXCLUDED_LABELS = ['closed', 'wontfix', 'duplicate', 'invalid'];
const DATA_DIR = path.join(__dirname, '..', 'data');
const BOUNTIES_FILE = path.join(DATA_DIR, 'bounties.json');

async function searchBounties(query, platform) {
  try {
    const result = await octokit.search.issuesAndPullRequests({
      q: query,
      sort: 'created',
      order: 'desc',
      per_page: 50
    });

    return result.data.items
      .filter(issue => !issue.pull_request)
      .filter(issue => {
        const labels = issue.labels.map(l => l.name.toLowerCase());
        return !EXCLUDED_LABELS.some(excluded => labels.includes(excluded));
      })
      .map(issue => ({
        id: issue.id,
        title: issue.title,
        url: issue.html_url,
        repository: issue.repository_url.replace('https://api.github.com/repos/', ''),
        state: issue.state,
        created_at: issue.created_at,
        updated_at: issue.updated_at,
        labels: issue.labels.map(l => l.name),
        platform: platform,
        body: issue.body ? issue.body.substring(0, 500) : ''
      }));
  } catch (error) {
    console.error(`Error searching bounties for ${platform}:`, error.message);
    return [];
  }
}

async function loadExistingBounties() {
  try {
    const data = await fs.readFile(BOUNTIES_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    if (error.code === 'ENOENT') {
      return { bounties: [], last_updated: null };
    }
    throw error;
  }
}

async function saveBounties(data) {
  try {
    await fs.mkdir(DATA_DIR, { recursive: true });
    await fs.writeFile(BOUNTIES_FILE, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error saving bounties:', error.message);
    throw error;
  }
}

async function createOrUpdateIssue(newBounties, totalBounties) {
  const owner = process.env.GITHUB_REPOSITORY?.split('/')[0] || 'dev-kp-eloper';
  const repo = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'BountyScout';

  if (!owner || !repo) {
    console.log('Repository information not available, skipping issue creation');
    return;
  }

  const title = `🎯 Bounty Alert: ${newBounties.length} New Opportunit${newBounties.length === 1 ? 'y' : 'ies'} Found`;
  
  let body = `## 🎉 New Bounty Opportunities\n\n`;
  body += `Found **${newBounties.length}** new bounty opportunit${newBounties.length === 1 ? 'y' : 'ies'}!\n\n`;
  body += `Total tracked bounties: **${totalBounties}**\n\n`;
  body += `---\n\n`;

  if (newBounties.length > 0) {
    const groupedByPlatform = newBounties.reduce((acc, bounty) => {
      if (!acc[bounty.platform]) acc[bounty.platform] = [];
      acc[bounty.platform].push(bounty);
      return acc;
    }, {});

    for (const [platform, bounties] of Object.entries(groupedByPlatform)) {
      body += `### ${platform}\n\n`;
      bounties.slice(0, 10).forEach(bounty => {
        body += `- **[${bounty.title}](${bounty.url})**\n`;
        body += `  - Repository: \`${bounty.repository}\`\n`;
        body += `  - Created: ${new Date(bounty.created_at).toLocaleDateString()}\n`;
        if (bounty.labels.length > 0) {
          body += `  - Labels: ${bounty.labels.map(l => `\`${l}\``).join(', ')}\n`;
        }
        body += `\n`;
      });
      if (bounties.length > 10) {
        body += `_...and ${bounties.length - 10} more_\n\n`;
      }
    }
  }

  body += `---\n\n`;
  body += `*Last updated: ${new Date().toISOString()}*\n`;
  body += `*Automated by BountyScout 🤖*`;

  try {
    const { data: issues } = await octokit.issues.listForRepo({
      owner,
      repo,
      state: 'open',
      labels: 'bounty-alert',
      per_page: 1
    });

    if (issues.length > 0 && newBounties.length > 0) {
      await octokit.issues.update({
        owner,
        repo,
        issue_number: issues[0].number,
        title,
        body
      });
      console.log(`Updated issue #${issues[0].number}`);
    } else if (newBounties.length > 0) {
      const { data: issue } = await octokit.issues.create({
        owner,
        repo,
        title,
        body,
        labels: ['bounty-alert']
      });
      console.log(`Created issue #${issue.number}`);
    }
  } catch (error) {
    console.error('Error creating/updating issue:', error.message);
  }
}

async function main() {
  console.log('🔍 Starting Bounty Scout...');

  const existingData = await loadExistingBounties();
  const existingIds = new Set(existingData.bounties.map(b => b.id));

  const allBounties = [];
  
  for (const platform of BOUNTY_PLATFORMS) {
    console.log(`Searching ${platform.name}...`);
    const bounties = await searchBounties(platform.query, platform.name);
    allBounties.push(...bounties);
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  const uniqueBounties = Array.from(
    new Map(allBounties.map(b => [b.id, b])).values()
  );

  const newBounties = uniqueBounties.filter(b => !existingIds.has(b.id));

  console.log(`Found ${uniqueBounties.length} total bounties`);
  console.log(`${newBounties.length} new bounties`);

  const updatedData = {
    bounties: uniqueBounties,
    last_updated: new Date().toISOString(),
    stats: {
      total: uniqueBounties.length,
      new: newBounties.length,
      by_platform: BOUNTY_PLATFORMS.reduce((acc, p) => {
        acc[p.name] = uniqueBounties.filter(b => b.platform === p.name).length;
        return acc;
      }, {})
    }
  };

  await saveBounties(updatedData);

  if (newBounties.length > 0) {
    await createOrUpdateIssue(newBounties, uniqueBounties.length);
  }

  console.log('✅ Bounty Scout completed!');
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { main, searchBounties };
