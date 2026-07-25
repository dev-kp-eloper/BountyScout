require('dotenv').config();
const BountyScout = require('./scout');
const NotificationService = require('./notifications');
const StorageService = require('./storage');

async function main() {
  try {
    console.log('🔍 Starting Bounty Scout...');
    
    const storage = new StorageService();
    const scout = new BountyScout(process.env.GITHUB_TOKEN);
    const notifier = new NotificationService({
      discordWebhook: process.env.DISCORD_WEBHOOK_URL,
      slackWebhook: process.env.SLACK_WEBHOOK_URL
    });

    // Load previously found bounties
    const previousBounties = await storage.load();
    console.log(`📦 Loaded ${previousBounties.length} previous bounties`);

    // Search for new bounties
    const allBounties = await scout.findBounties();
    console.log(`🎯 Found ${allBounties.length} total bounties`);

    // Filter out already notified bounties
    const newBounties = allBounties.filter(
      bounty => !previousBounties.some(prev => prev.id === bounty.id)
    );

    if (newBounties.length > 0) {
      console.log(`✨ ${newBounties.length} new opportunities found!`);
      
      // Send notifications
      await notifier.sendNotification(newBounties);
      
      // Update storage
      await storage.save(allBounties);
      
      console.log('✅ Notifications sent successfully');
    } else {
      console.log('ℹ️  No new bounties found');
    }

  } catch (error) {
    console.error('❌ Error running Bounty Scout:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = main;