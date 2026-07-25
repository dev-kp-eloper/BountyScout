const axios = require('axios');

class NotificationService {
  constructor(config) {
    this.discordWebhook = config.discordWebhook;
    this.slackWebhook = config.slackWebhook;
  }

  async sendNotification(bounties) {
    const promises = [];

    if (this.discordWebhook) {
      promises.push(this.sendDiscordNotification(bounties));
    }

    if (this.slackWebhook) {
      promises.push(this.sendSlackNotification(bounties));
    }

    if (promises.length === 0) {
      console.log('ℹ️  No notification webhooks configured');
      return;
    }

    await Promise.allSettled(promises);
  }

  async sendDiscordNotification(bounties) {
    try {
      const count = bounties.length;
      const title = `🎯 Bounty Alert: ${count} New ${count === 1 ? 'Opportunity' : 'Opportunities'} Found`;
      
      const embeds = bounties.slice(0, 10).map(bounty => ({
        title: bounty.title,
        url: bounty.url,
        description: this.truncate(bounty.body, 200),
        color: 0x00ff00,
        fields: [
          {
            name: '📦 Repository',
            value: bounty.repository,
            inline: true
          },
          {
            name: '👤 Author',
            value: bounty.author,
            inline: true
          },
          {
            name: '🏷️ Labels',
            value: bounty.labels.length > 0 ? bounty.labels.join(', ') : 'None',
            inline: false
          }
        ],
        timestamp: bounty.createdAt
      }));

      await axios.post(this.discordWebhook, {
        content: title,
        embeds: embeds
      });

      console.log('✅ Discord notification sent');
    } catch (error) {
      console.error('❌ Error sending Discord notification:', error.message);
    }
  }

  async sendSlackNotification(bounties) {
    try {
      const count = bounties.length;
      const title = `🎯 Bounty Alert: ${count} New ${count === 1 ? 'Opportunity' : 'Opportunities'} Found`;
      
      const blocks = [
        {
          type: 'header',
          text: {
            type: 'plain_text',
            text: title
          }
        },
        {
          type: 'divider'
        }
      ];

      for (const bounty of bounties.slice(0, 10)) {
        blocks.push(
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: `*<${bounty.url}|${bounty.title}>*\n${this.truncate(bounty.body, 150)}`
            }
          },
          {
            type: 'context',
            elements: [
              {
                type: 'mrkdwn',
                text: `📦 ${bounty.repository} | 👤 ${bounty.author} | 🏷️ ${bounty.labels.join(', ') || 'None'}`
              }
            ]
          },
          {
            type: 'divider'
          }
        );
      }

      await axios.post(this.slackWebhook, {
        blocks: blocks
      });

      console.log('✅ Slack notification sent');
    } catch (error) {
      console.error('❌ Error sending Slack notification:', error.message);
    }
  }

  truncate(text, maxLength) {
    if (!text) return 'No description provided';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }
}

module.exports = NotificationService;