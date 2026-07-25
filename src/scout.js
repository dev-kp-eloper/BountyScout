const { Octokit } = require('@octokit/rest');

class BountyScout {
  constructor(githubToken) {
    this.octokit = new Octokit({
      auth: githubToken
    });
    
    this.bountyKeywords = [
      'bounty',
      'reward',
      'prize',
      'hackathon',
      'bug bounty',
      'security bounty',
      'cash prize'
    ];
  }

  async findBounties() {
    const bounties = [];
    
    try {
      // Search for issues with bounty-related labels
      const labelQueries = [
        'label:bounty',
        'label:"bug bounty"',
        'label:reward',
        'label:prize',
        'label:hackathon'
      ];

      for (const labelQuery of labelQueries) {
        try {
          const { data } = await this.octokit.search.issuesAndPullRequests({
            q: `${labelQuery} is:issue is:open`,
            sort: 'created',
            order: 'desc',
            per_page: 50
          });

          for (const issue of data.items) {
            if (!bounties.some(b => b.id === issue.id)) {
              bounties.push(this.formatBounty(issue));
            }
          }
        } catch (error) {
          console.warn(`⚠️  Error searching with query "${labelQuery}":`, error.message);
        }
      }

      // Search for issues with bounty keywords in title/body
      for (const keyword of this.bountyKeywords) {
        try {
          const { data } = await this.octokit.search.issuesAndPullRequests({
            q: `"${keyword}" in:title,body is:issue is:open`,
            sort: 'created',
            order: 'desc',
            per_page: 30
          });

          for (const issue of data.items) {
            if (!bounties.some(b => b.id === issue.id) && this.isBountyIssue(issue)) {
              bounties.push(this.formatBounty(issue));
            }
          }
        } catch (error) {
          console.warn(`⚠️  Error searching for keyword "${keyword}":`, error.message);
        }

        // Rate limiting delay
        await this.sleep(1000);
      }

      return bounties;
    } catch (error) {
      console.error('❌ Error finding bounties:', error.message);
      throw error;
    }
  }

  isBountyIssue(issue) {
    const text = `${issue.title} ${issue.body || ''}`.toLowerCase();
    
    // Check for monetary indicators
    const hasMonetary = /\$\d+|€\d+|£\d+|\d+\s*(usd|eur|gbp|dollars?|euros?|pounds?)/.test(text);
    
    // Check for bounty keywords
    const hasBountyKeyword = this.bountyKeywords.some(keyword => 
      text.includes(keyword.toLowerCase())
    );
    
    return hasMonetary || hasBountyKeyword;
  }

  formatBounty(issue) {
    return {
      id: issue.id,
      title: issue.title,
      url: issue.html_url,
      repository: issue.repository_url.split('/').slice(-2).join('/'),
      labels: issue.labels.map(l => l.name),
      createdAt: issue.created_at,
      author: issue.user.login,
      body: issue.body ? issue.body.substring(0, 500) : '',
      state: issue.state
    };
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = BountyScout;