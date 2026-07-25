const fs = require('fs').promises;
const path = require('path');

class StorageService {
  constructor() {
    this.storageDir = path.join(process.cwd(), 'data');
    this.storageFile = path.join(this.storageDir, 'bounties.json');
  }

  async load() {
    try {
      await fs.mkdir(this.storageDir, { recursive: true });
      
      const data = await fs.readFile(this.storageFile, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return [];
      }
      console.error('❌ Error loading storage:', error.message);
      return [];
    }
  }

  async save(bounties) {
    try {
      await fs.mkdir(this.storageDir, { recursive: true });
      
      // Keep only the last 1000 bounties to prevent file from growing too large
      const bounciesToSave = bounties.slice(-1000);
      
      await fs.writeFile(
        this.storageFile,
        JSON.stringify(bounciesToSave, null, 2),
        'utf8'
      );
      
      console.log(`💾 Saved ${bounciesToSave.length} bounties to storage`);
    } catch (error) {
      console.error('❌ Error saving storage:', error.message);
      throw error;
    }
  }
}

module.exports = StorageService;