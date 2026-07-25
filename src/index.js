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
    url: 'https://yeswehack.com/programs',
    type: 'yeswehack'
  }
];

const DATA_FILE = path.join(__dirname, '..', 'data', 'bounties.json');
const NEW_BOUNTIES_FILE = path.join(__dirname, '..', 'data', 'new-bounties.json');

class BountyScout {
  constructor() {
    this.existingBounties = [];
    this.newBounties = [];
  }

  async loadExistingBounties() {
    try {
      const data = await fs.readFile(DATA_FILE, 'utf8');
      this.existingBounties = JSON.parse(data);
      console.log(`Loaded ${this.existingBounties.length} existing bounties`);
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.log('No existing bounties file found, starting fresh');
        this.existingBounties = [];
      } else {
        throw error;
      }
    }
  }

  async scrapeBounties() {
    const allBounties = [];

    for (const platform of PLATFORMS) {
      try {
        console.log(`Scraping ${platform.name}...`);
        const bounties = await this.scrapePlatform(platform);
        allBounties.push(...bounties);
        console.log(`Found ${bounties.length} bounties on ${platform.name}`);
      } catch (error) {
        console.error(`Error scraping ${platform.name}:`, error.message);
      }
    }

    return allBounties;
  }

  async scrapePlatform(platform) {
    // Simulate scraping with mock data for demonstration
    // In production, implement actual scraping logic for each platform
    const mockBounties = this.generateMockBounties(platform);
    return mockBounties;
  }

  generateMockBounties(platform) {
    const bounties = [];
    const count = Math.floor(Math.random() * 25) + 5;

    for (let i = 0; i < count; i++) {
      const bounty = {
        id: `${platform.type}-${Date.now()}-${i}`,
        platform: platform.name,
        title: `${platform.name} Program ${i + 1}`,
        company: `Company ${String.fromCharCode(65 + (i % 26))}`,
        minBounty: Math.floor(Math.random() * 1000) + 100,
        maxBounty: Math.floor(Math.random() * 10000) + 5000,
        url: `${platform.url}/${i}`,
        discoveredAt: new Date().toISOString(),
        scope: ['Web Application', 'API', 'Mobile App'][Math.floor(Math.random() * 3)],
        status: 'active'
      };
      bounties.push(bounty);
    }

    return bounties;
  }

  findNewBounties(scrapedBounties) {
    const existingIds = new Set(this.existingBounties.map(b => b.id));
    this.newBounties = scrapedBounties.filter(bounty => !existingIds.has(bounty.id));
    console.log(`Found ${this.newBounties.length} new bounties`);
    return this.newBounties;
  }

  async saveData(allBounties) {
    try {
      await fs.mkdir(path.dirname(DATA_FILE), { recursive: true });
      
      // Save all bounties
      await fs.writeFile(DATA_FILE, JSON.stringify(allBounties, null, 2));
      console.log(`Saved ${allBounties.length} total bounties`);

      // Save new bounties separately for issue creation
      await fs.writeFile(NEW_BOUNTIES_FILE, JSON.stringify(this.newBounties, null, 2));
      console.log(`Saved ${this.newBounties.length} new bounties`);
    } catch (error) {
      console.error('Error saving data:', error);
      throw error;
    }
  }

  async run() {
    try {
      console.log('Starting Bounty Scout...');
      
      await this.loadExistingBounties();
      const scrapedBounties = await this.scrapeBounties();
      this.findNewBounties(scrapedBounties);
      
      // Merge existing and new bounties, removing duplicates
      const allBounties = [...this.existingBounties];
      for (const newBounty of this.newBounties) {
        if (!allBounties.find(b => b.id === newBounty.id)) {
          allBounties.push(newBounty);
        }
      }

      await this.saveData(allBounties);
      
      console.log('Bounty Scout completed successfully');
      console.log(`Total bounties: ${allBounties.length}`);
      console.log(`New bounties: ${this.newBounties.length}`);
    } catch (error) {
      console.error('Error running Bounty Scout:', error);
      process.exit(1);
    }
  }
}

if (require.main === module) {
  const scout = new BountyScout();
  scout.run();
}

module.exports = BountyScout;