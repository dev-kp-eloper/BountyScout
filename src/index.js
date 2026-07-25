const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

const PLATFORMS = [
  {
    name: 'HackerOne',
    url: 'https://hackerone.com/opportunities/all',
    type: 'hackerone'
  },
  {
    name: 'Bugcrowd',
    url: 'https://bugcrowd.com/programs',
    type: 'bugcrowd'
  },
  {
    name: 'Intigriti',
    url: 'https://www.intigriti.com/programs',
    type: 'intigriti'
  },
  {
    name: 'YesWeHack',
    url: 'https://www.yeswehack.com/programs',
    type: 'yeswehack'
  }
];

const DATA_DIR = path.join(__dirname, '..', 'data');
const BOUNTIES_FILE = path.join(DATA_DIR, 'bounties.json');
const NEW_BOUNTIES_FILE = path.join(DATA_DIR, 'new-bounties.json');

class BountyScout {
  constructor() {
    this.existingBounties = [];
    this.newBounties = [];
  }

  async init() {
    try {
      await fs.mkdir(DATA_DIR, { recursive: true });
      
      try {
        const data = await fs.readFile(BOUNTIES_FILE, 'utf8');
        this.existingBounties = JSON.parse(data);
      } catch (error) {
        if (error.code !== 'ENOENT') {
          throw error;
        }
        this.existingBounties = [];
      }
    } catch (error) {
      console.error('Error initializing BountyScout:', error.message);
      throw error;
    }
  }

  async scrapeBounties() {
    console.log('Starting bounty scout...');
    const allBounties = [];

    for (const platform of PLATFORMS) {
      try {
        console.log(`Fetching bounties from ${platform.name}...`);
        const bounties = await this.fetchBountiesFromPlatform(platform);
        allBounties.push(...bounties);
        console.log(`Found ${bounties.length} bounties on ${platform.name}`);
      } catch (error) {
        console.error(`Error fetching from ${platform.name}:`, error.message);
      }
    }

    return allBounties;
  }

  async fetchBountiesFromPlatform(platform) {
    // Simulate fetching bounties from different platforms
    // In production, this would make actual API calls or web scraping
    const mockBounties = this.generateMockBounties(platform);
    return mockBounties;
  }

  generateMockBounties(platform) {
    const bounties = [];
    const numBounties = Math.floor(Math.random() * 25) + 5;

    for (let i = 0; i < numBounties; i++) {
      const bounty = {
        id: `${platform.type}-${Date.now()}-${i}`,
        platform: platform.name,
        title: `Bug Bounty Program ${i + 1}`,
        company: `Company ${String.fromCharCode(65 + (i % 26))}`,
        url: `${platform.url}/${i + 1}`,
        minBounty: Math.floor(Math.random() * 1000) + 100,
        maxBounty: Math.floor(Math.random() * 10000) + 5000,
        discoveredAt: new Date().toISOString()
      };
      bounties.push(bounty);
    }

    return bounties;
  }

  findNewBounties(allBounties) {
    const existingIds = new Set(this.existingBounties.map(b => b.id));
    this.newBounties = allBounties.filter(bounty => !existingIds.has(bounty.id));
    return this.newBounties;
  }

  async saveBounties(allBounties) {
    try {
      await fs.writeFile(
        BOUNTIES_FILE,
        JSON.stringify(allBounties, null, 2),
        'utf8'
      );
      console.log(`Saved ${allBounties.length} bounties to database`);

      if (this.newBounties.length > 0) {
        await fs.writeFile(
          NEW_BOUNTIES_FILE,
          JSON.stringify(this.newBounties, null, 2),
          'utf8'
        );
        console.log(`Saved ${this.newBounties.length} new bounties`);
      }
    } catch (error) {
      console.error('Error saving bounties:', error.message);
      throw error;
    }
  }

  async run() {
    try {
      await this.init();
      const allBounties = await this.scrapeBounties();
      const newBounties = this.findNewBounties(allBounties);
      
      console.log(`\nTotal bounties found: ${allBounties.length}`);
      console.log(`New bounties: ${newBounties.length}`);

      await this.saveBounties(allBounties);

      return {
        total: allBounties.length,
        new: newBounties.length,
        bounties: newBounties
      };
    } catch (error) {
      console.error('Error running BountyScout:', error.message);
      throw error;
    }
  }
}

if (require.main === module) {
  const scout = new BountyScout();
  scout.run()
    .then(result => {
      console.log('\nBounty scout completed successfully!');
      process.exit(0);
    })
    .catch(error => {
      console.error('\nBounty scout failed:', error);
      process.exit(1);
    });
}

module.exports = BountyScout;