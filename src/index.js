const { Octokit } = require('@octokit/rest');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_SOURCES = [
  {
    name: 'HackerOne',
    url: 'https://hackerone.com/directory/programs',
    type: 'web'
  },
  {
    name: 'Bugcrowd',
    url: 'https://bugcrowd.com/programs',
    type: 'web'
  },
  {
    name: 'GitHub Issues',
    type: 'github'
  }
];

const BOUNTY_KEYWORDS = [
  'bounty',
  'bug bounty',
  'security bounty',
  'reward',
  'vulnerability reward',
  'security reward',
  'bug reward'
];

class BountyScout {
  constructor() {
    this.dataFile = path.join(__dirname, '..', 'data', 'bounties.json');
    this.previousBounties = [];
    this.newBounties = [];
  }

  async initialize() {
    try {
      await fs.mkdir(path.join(__dirname, '..', 'data'), { recursive: true });
      const data = await fs.readFile(this.dataFile, 'utf8');
      this.previousBounties = JSON.parse(data);
    } catch (error) {
      if (error.code === 'ENOENT') {
        this.previousBounties = [];
      } else {
        console.error('Error loading previous bounties:', error.message);
        this.previousBounties = [];
      }
    }
  }

  async searchGitHubIssues() {
    const bounties = [];
    
    try {
      for (const keyword of BOUNTY_KEYWORDS) {
        const query = `${keyword} in:title,body is:issue is:open label:bounty,bug-bounty`;
        
        try {
          const response = await octokit.search.issuesAndPullRequests({
            q: query,
            sort: 'created',
            order: 'desc',
            per_page: 30
          });

          for (const issue of response.data.items) {
            if (!issue.pull_request) {
              const bountyData = {
                id: `github-${issue.id}`,
                title: issue.title,
                url: issue.html_url,
                source: 'GitHub',
                repository: issue.repository_url.replace('https://api.github.com/repos/', ''),
                created_at: issue.created_at,
                labels: issue.labels.map(l => l.name),
                description: issue.body ? issue.body.substring(0, 200) : ''
              };
              
              if (!bounties.find(b => b.id === bountyData.id)) {
                bounties.push(bountyData);
              }
            }
          }

          // Rate limiting
          await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (error) {
          console.error(`Error searching for "${keyword}":`, error.message);
        }
      }
    } catch (error) {
      console.error('Error in GitHub search:', error.message);
    }

    return bounties;
  }

  async searchBountyPlatforms() {
    const bounties = [];
    
    // Search for repositories with bounty programs
    try {
      const response = await octokit.search.repos({
        q: 'bug bounty security.txt in:readme',
        sort: 'updated',
        order: 'desc',
        per_page: 20
      });

      for (const repo of response.data.items) {
        const bountyData = {
          id: `repo-${repo.id}`,
          title: `${repo.full_name} - Bug Bounty Program`,
          url: repo.html_url,
          source: 'GitHub Repository',
          repository: repo.full_name,
          created_at: repo.updated_at,
          labels: ['bug-bounty', 'security'],
          description: repo.description || 'Repository with bug bounty program'
        };
        
        bounties.push(bountyData);
      }
    } catch (error) {
      console.error('Error searching bounty platforms:', error.message);
    }

    return bounties;
  }

  findNewBounties(allBounties) {
    const previousIds = new Set(this.previousBounties.map(b => b.id));
    return allBounties.filter(bounty => !previousIds.has(bounty.id));
  }

  async saveBounties(bounties) {
    try {
      await fs.writeFile(this.dataFile, JSON.stringify(bounties, null, 2));
      console.log(`Saved ${bounties.length} bounties to database`);
    } catch (error) {
      console.error('Error saving bounties:', error.message);
    }
  }

  async run() {
    console.log('🔍 Starting Bounty Scout...');
    
    await this.initialize();
    
    console.log('🔎 Searching GitHub issues...');
    const githubBounties = await this.searchGitHubIssues();
    console.log(`Found ${githubBounties.length} bounties from GitHub issues`);
    
    console.log('🔎 Searching bounty platforms...');
    const platformBounties = await this.searchBountyPlatforms();
    console.log(`Found ${platformBounties.length} bounties from platforms`);
    
    const allBounties = [...githubBounties, ...platformBounties];
    
    // Remove duplicates
    const uniqueBounties = Array.from(
      new Map(allBounties.map(b => [b.id, b])).values()
    );
    
    console.log(`Total unique bounties: ${uniqueBounties.length}`);
    
    this.newBounties = this.findNewBounties(uniqueBounties);
    console.log(`🎯 Found ${this.newBounties.length} new bounties!`);
    
    // Merge with previous bounties
    const updatedBounties = [...this.previousBounties, ...this.newBounties];
    
    // Keep only last 1000 bounties to prevent file from growing too large
    const bounciesToSave = updatedBounties.slice(-1000);
    
    await this.saveBounties(bounciesToSave);
    
    // Save new bounties for issue creation
    if (this.newBounties.length > 0) {
      await fs.writeFile(
        path.join(__dirname, '..', 'data', 'new-bounties.json'),
        JSON.stringify(this.newBounties, null, 2)
      );
    }
    
    console.log('✅ Bounty Scout completed!');
    return this.newBounties;
  }
}

if (require.main === module) {
  const scout = new BountyScout();
  scout.run().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = BountyScout;