const axios = require('axios');

const NOTIFICATION_WEBHOOK = process.env.NOTIFICATION_WEBHOOK;

async function sendNotification(data) {
  if (!NOTIFICATION_WEBHOOK) {
    console.log('ℹ️ No notification webhook configured');
    return;
  }
  
  try {
    const message = formatNotificationMessage(data);
    
    // Support for different webhook types
    if (NOTIFICATION_WEBHOOK.includes('slack.com')) {
      await sendSlackNotification(message);
    } else if (NOTIFICATION_WEBHOOK.includes('discord.com')) {
      await sendDiscordNotification(message);
    } else {
      await sendGenericWebhook(message);
    }
    
    console.log('✅ Notification sent successfully');
  } catch (error) {
    console.error('❌ Error sending notification:', error.message);
  }
}

function formatNotificationMessage(data) {
  let message = `${data.title}\n\n`;
  
  if (data.bounties && data.bounties.length > 0) {
    message += 'Top opportunities:\n';
    
    for (const bounty of data.bounties.slice(0, 5)) {
      message += `\n• ${bounty.title}\n`;
      message += `  Repository: ${bounty.repository}\n`;
      message += `  URL: ${bounty.url}\n`;
    }
  }
  
  message += `\nTotal active bounties: ${data.total}`;
  
  return message;
}

async function sendSlackNotification(message) {
  await axios.post(NOTIFICATION_WEBHOOK, {
    text: message,
    mrkdwn: true
  });
}

async function sendDiscordNotification(message) {
  await axios.post(NOTIFICATION_WEBHOOK, {
    content: message
  });
}

async function sendGenericWebhook(message) {
  await axios.post(NOTIFICATION_WEBHOOK, {
    message: message,
    timestamp: new Date().toISOString()
  });
}

module.exports = {
  sendNotification
};
