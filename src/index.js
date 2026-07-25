const { Octokit } = require('@octokit/rest');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_PLATFORMS = [
  {
    name: 'GitHub',
    search: async () => {
      try {
        const { data } = await octokit.search.issuesAndPullRequests({
          q: 'label:bounty,bug-bounty,"bug bounty" state:open is:issue',
          sort: 'created',
          order: 'desc',
          per_page: 50
        });
        return data.items.map(item => ({
          title: item.title,
          url: item.html_url,
          platform: 'GitHub',
          repository: item.repository_url.split('/').slice(-2).join('/'),
          created_at: item.created_at,
          labels: item.labels.map(l => l.name),
          id: `github-${item.id}`
        }));
      } catch (error) {
        console.error('Error fetching GitHub bounties:', error.message);
        return [];
      }
    }
  },
  {
    name: 'Gitcoin',
    search: async () => {
      try {
        const response = await axios.get('https://gitcoin.co/api/v0.1/bounties/', {
          params: {
            network: 'mainnet',
            order_by: '-web3_created',
            idx_status: 'open'
          },
          timeout: 10000
        });
        return response.data.slice(0, 20).map(bounty => ({
          title: bounty.title,
          url: bounty.url,
          platform: 'Gitcoin',
          value: bounty.value_in_usdt,
          created_at: bounty.web3_created,
          id: `gitcoin-${bounty.id}`
        }));
      } catch (error) {
        console.error('Error fetching Gitcoin bounties:', error.message);
        return [];
      }
    }
  }
];

async function loadPreviousBounties() {
  try {
    const dataPath = path.join(__dirname, '..', 'data', 'bounties.json');
    const data = await fs.readFile(dataPath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return { bounties: [], lastChecked: null };
  }
}

async function saveBounties(bounties) {
  try {
    const dataPath = path.join(__dirname, '..', 'data', 'bounties.json');
    await fs.mkdir(path.dirname(dataPath), { recursive: true });
    await fs.writeFile(dataPath, JSON.stringify({
      bounties,
      lastChecked: new Date().toISOString()
    }, null, 2));
  } catch (error) {
    console.error('Error saving bounties:', error.message);
  }
}

async function findNewBounties() {
  console.log('🔍 Scouting for new bounty opportunities...');
  
  const previousData = await loadPreviousBounties();
  const previousIds = new Set(previousData.bounties.map(b => b.id));
  
  const allBounties = [];
  
  for (const platform of BOUNTY_PLATFORMS) {
    console.log(`Searching ${platform.name}...`);
    const bounties = await platform.search();
    allBounties.push(...bounties);
  }
  
  const newBounties = allBounties.filter(bounty => !previousIds.has(bounty.id));
  
  console.log(`✅ Found ${allBounties.length} total bounties`);
  console.log(`🎯 ${newBounties.length} new opportunities discovered!`);
  
  if (newBounties.length > 0) {
    await saveBounties(allBounties);
    await saveNewBountiesReport(newBounties);
  }
  
  return newBounties;
}

async function saveNewBountiesReport(newBounties) {
  try {
    const reportPath = path.join(__dirname, '..', 'data', 'new-bounties.json');
    await fs.mkdir(path.dirname(reportPath), { recursive: true });
    await fs.writeFile(reportPath, JSON.stringify({
      count: newBounties.length,
      bounties: newBounties,
      timestamp: new Date().toISOString()
    }, null, 2));
  } catch (error) {
    console.error('Error saving new bounties report:', error.message);
  }
}

if (require.main === module) {
  findNewBounties()
    .then(() => {
      console.log('✨ Bounty scout completed successfully!');
      process.exit(0);
    })
    .catch(error => {
      console.error('❌ Error running bounty scout:', error);
      process.exit(1);
    });
}

module.exports = { findNewBounties };