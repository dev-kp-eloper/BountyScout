const { Octokit } = require('@octokit/rest');
const fs = require('fs').promises;
const path = require('path');

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_KEYWORDS = [
  'bounty',
  'reward',
  'prize',
  'hackathon',
  'bug bounty',
  'security bounty',
  'good first issue',
  'help wanted'
];

const BOUNTY_LABELS = [
  'bounty',
  'bug-bounty',
  'reward',
  'prize',
  'hackathon',
  'good first issue',
  'help wanted'
];

const DATA_FILE = path.join(__dirname, '..', 'data', 'bounties.json');
const ISSUE_TITLE_TYPO = 'Opportunityies';
const ISSUE_TITLE_CORRECT = 'Opportunities';

async function searchBountyIssues() {
  const allIssues = [];
  const queries = [
    'label:bounty state:open',
    'label:bug-bounty state:open',
    'label:reward state:open',
    'bounty in:title state:open',
    'reward in:title state:open'
  ];

  try {
    for (const query of queries) {
      const response = await octokit.search.issuesAndPullRequests({
        q: query,
        sort: 'created',
        order: 'desc',
        per_page: 100
      });

      allIssues.push(...response.data.items.filter(item => !item.pull_request));
    }

    // Remove duplicates based on issue URL
    const uniqueIssues = Array.from(
      new Map(allIssues.map(issue => [issue.html_url, issue])).values()
    );

    return uniqueIssues;
  } catch (error) {
    console.error('Error searching for bounty issues:', error.message);
    return [];
  }
}

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

async function saveBounties(bounties) {
  try {
    await fs.mkdir(path.dirname(DATA_FILE), { recursive: true });
    await fs.writeFile(
      DATA_FILE,
      JSON.stringify(
        {
          bounties,
          lastUpdated: new Date().toISOString()
        },
        null,
        2
      )
    );
  } catch (error) {
    console.error('Error saving bounties:', error.message);
  }
}

function extractBountyInfo(issue) {
  return {
    id: issue.id,
    title: issue.title,
    url: issue.html_url,
    repository: issue.repository_url.replace('https://api.github.com/repos/', ''),
    labels: issue.labels.map(label => label.name),
    createdAt: issue.created_at,
    updatedAt: issue.updated_at,
    state: issue.state,
    body: issue.body ? issue.body.substring(0, 500) : ''
  };
}

async function createOrUpdateIssue(newBounties) {
  try {
    const [owner, repo] = process.env.GITHUB_REPOSITORY?.split('/') || ['dev-kp-eloper', 'BountyScout'];
    
    // Search for existing bounty alert issues
    const existingIssues = await octokit.issues.listForRepo({
      owner,
      repo,
      state: 'open',
      labels: 'bounty-alert',
      per_page: 100
    });

    // Also search for issues with the typo in the title
    const allIssues = await octokit.issues.listForRepo({
      owner,
      repo,
      state: 'all',
      per_page: 100
    });

    const issuesWithTypo = allIssues.data.filter(issue => 
      issue.title.includes(ISSUE_TITLE_TYPO)
    );

    // Close issues with typo and add comment
    for (const issue of issuesWithTypo) {
      if (issue.state === 'open') {
        await octokit.issues.update({
          owner,
          repo,
          issue_number: issue.number,
          state: 'closed'
        });

        await octokit.issues.createComment({
          owner,
          repo,
          issue_number: issue.number,
          body: `This issue has been closed and replaced with a corrected version. The typo "${ISSUE_TITLE_TYPO}" has been fixed to "${ISSUE_TITLE_CORRECT}".`
        });
      }
    }

    if (newBounties.length === 0) {
      console.log('No new bounties found.');
      return;
    }

    const issueBody = `## 🎯 New Bounty ${ISSUE_TITLE_CORRECT} Found\n\n` +
      `Found **${newBounties.length}** new bounty ${newBounties.length === 1 ? 'opportunity' : 'opportunities'}!\n\n` +
      newBounties.map((bounty, index) => 
        `### ${index + 1}. ${bounty.title}\n` +
        `- **Repository:** ${bounty.repository}\n` +
        `- **URL:** ${bounty.url}\n` +
        `- **Labels:** ${bounty.labels.join(', ')}\n` +
        `- **Created:** ${new Date(bounty.createdAt).toLocaleDateString()}\n\n` +
        `${bounty.body ? `**Description:**\n${bounty.body}\n\n` : ''}` +
        `---\n\n`
      ).join('') +
      `\n\n*Last updated: ${new Date().toISOString()}*`;

    const issueTitle = `🎯 Bounty Alert: ${newBounties.length} New ${newBounties.length === 1 ? 'Opportunity' : ISSUE_TITLE_CORRECT} Found`;

    // Create new issue with corrected spelling
    await octokit.issues.create({
      owner,
      repo,
      title: issueTitle,
      body: issueBody,
      labels: ['bounty-alert', 'automated']
    });

    console.log(`Created new issue: ${issueTitle}`);
  } catch (error) {
    console.error('Error creating/updating issue:', error.message);
  }
}

async function main() {
  console.log('Starting Bounty Scout...');

  const issues = await searchBountyIssues();
  console.log(`Found ${issues.length} total bounty issues`);

  const existingData = await loadExistingBounties();
  const existingIds = new Set(existingData.bounties.map(b => b.id));

  const newBounties = issues
    .filter(issue => !existingIds.has(issue.id))
    .map(extractBountyInfo);

  console.log(`Found ${newBounties.length} new bounties`);

  if (newBounties.length > 0) {
    const allBounties = [...existingData.bounties, ...newBounties];
    await saveBounties(allBounties);
    await createOrUpdateIssue(newBounties);
  }

  console.log('Bounty Scout completed successfully!');
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { main, searchBountyIssues, extractBountyInfo };
