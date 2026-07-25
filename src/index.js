const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

const DATA_FILE = path.join(__dirname, '..', 'data', 'bounties.json');
const SOURCES = [
  {
    name: 'HackerOne',
    url: 'https://hackerone.com/directory/programs',
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
  }
];

class BountyScout {
  constructor() {
    this.existingBounties = new Set();
    this.newBounties = [];
  }

  async loadExistingBounties() {
    try {
      const data = await fs.readFile(DATA_FILE, 'utf8');
      const bounties = JSON.parse(data);
      this.existingBounties = new Set(bounties.map(b => b.id));
      console.log(`Loaded ${this.existingBounties.size} existing bounties`);
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.log('No existing bounties file found, starting fresh');
        await this.ensureDataDirectory();
      } else {
        console.error('Error loading existing bounties:', error.message);
      }
    }
  }

  async ensureDataDirectory() {
    const dataDir = path.join(__dirname, '..', 'data');
    try {
      await fs.mkdir(dataDir, { recursive: true });
    } catch (error) {
      console.error('Error creating data directory:', error.message);
    }
  }

  async scrapeBounties() {
    console.log('Starting bounty scout...');
    
    for (const source of SOURCES) {
      try {
        console.log(`Checking ${source.name}...`);
        await this.checkSource(source);
      } catch (error) {
        console.error(`Error checking ${source.name}:`, error.message);
      }
    }

    console.log(`Found ${this.newBounties.length} new bounties`);
    return this.newBounties;
  }

  async checkSource(source) {
    // Simulate finding bounties (in production, this would scrape actual sites)
    // For demonstration, we'll generate mock data
    const mockBounties = this.generateMockBounties(source);
    
    for (const bounty of mockBounties) {
      if (!this.existingBounties.has(bounty.id)) {
        this.newBounties.push(bounty);
        this.existingBounties.add(bounty.id);
      }
    }
  }

  generateMockBounties(source) {
    const bounties = [];
    const count = Math.floor(Math.random() * 10) + 1;
    
    for (let i = 0; i < count; i++) {
      const id = `${source.type}-${Date.now()}-${i}-${Math.random().toString(36).substr(2, 9)}`;
      bounties.push({
        id,
        title: `${source.name} Program ${i + 1}`,
        platform: source.name,
        url: `${source.url}/${id}`,
        reward: `$${(Math.random() * 10000 + 1000).toFixed(0)}`,
        severity: ['Critical', 'High', 'Medium', 'Low'][Math.floor(Math.random() * 4)],
        discoveredAt: new Date().toISOString()
      });
    }
    
    return bounties;
  }

  async saveBounties() {
    try {
      await this.ensureDataDirectory();
      
      let allBounties = [];
      try {
        const data = await fs.readFile(DATA_FILE, 'utf8');
        allBounties = JSON.parse(data);
      } catch (error) {
        // File doesn't exist, start with empty array
      }

      allBounties.push(...this.newBounties);
      
      await fs.writeFile(DATA_FILE, JSON.stringify(allBounties, null, 2));
      console.log('Bounties saved successfully');
    } catch (error) {
      console.error('Error saving bounties:', error.message);
      throw error;
    }
  }

  async saveNewBountiesReport() {
    try {
      const reportPath = path.join(__dirname, '..', 'data', 'new-bounties.json');
      await fs.writeFile(reportPath, JSON.stringify({
        count: this.newBounties.length,
        bounties: this.newBounties,
        timestamp: new Date().toISOString()
      }, null, 2));
      console.log('New bounties report saved');
    } catch (error) {
      console.error('Error saving report:', error.message);
    }
  }
}

async function main() {
  try {
    const scout = new BountyScout();
    await scout.loadExistingBounties();
    await scout.scrapeBounties();
    
    if (scout.newBounties.length > 0) {
      await scout.saveBounties();
      await scout.saveNewBountiesReport();
      console.log(`\n✅ Successfully found ${scout.newBounties.length} new opportunities!`);
    } else {
      console.log('\nℹ️  No new bounties found');
    }
  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = BountyScout;