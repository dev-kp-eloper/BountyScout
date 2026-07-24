const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification Service for BountyScout
 * Handles sending notifications about new bounty opportunities
 */
class NotificationService {
  constructor(config = {}) {
    this.config = {
      enabled: config.enabled !== undefined ? config.enabled : true,
      channels: config.channels || ['console'],
      ...config
    };
  }

  /**
   * Send notification about new bounty opportunities
   * @param {number} count - Number of new opportunities
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Promise<void>}
   */
  async sendBountyAlert(count, opportunities = []) {
    if (!this.config.enabled) {
      return;
    }

    try {
      const message = formatBountyNotification(count);
      
      for (const channel of this.config.channels) {
        await this._sendToChannel(channel, message, opportunities);
      }
    } catch (error) {
      console.error('Error sending bounty alert:', error.message);
      throw error;
    }
  }

  /**
   * Send notification to specific channel
   * @private
   * @param {string} channel - Channel name
   * @param {string} message - Notification message
   * @param {Array} opportunities - Array of opportunity objects
   */
  async _sendToChannel(channel, message, opportunities) {
    switch (channel) {
      case 'console':
        console.log(message);
        if (opportunities.length > 0) {
          console.log('Opportunities:', opportunities);
        }
        break;
      
      case 'slack':
        await this._sendToSlack(message, opportunities);
        break;
      
      case 'discord':
        await this._sendToDiscord(message, opportunities);
        break;
      
      case 'email':
        await this._sendEmail(message, opportunities);
        break;
      
      default:
        console.warn(`Unknown notification channel: ${channel}`);
    }
  }

  /**
   * Send notification to Slack
   * @private
   */
  async _sendToSlack(message, opportunities) {
    if (!this.config.slackWebhookUrl) {
      console.warn('Slack webhook URL not configured');
      return;
    }

    const payload = {
      text: message,
      attachments: opportunities.map(opp => ({
        title: opp.title || 'Untitled Opportunity',
        text: opp.description || '',
        fields: [
          {
            title: 'Reward',
            value: opp.reward || 'N/A',
            short: true
          },
          {
            title: 'Platform',
            value: opp.platform || 'Unknown',
            short: true
          }
        ],
        color: '#36a64f',
        footer: 'BountyScout',
        ts: Math.floor(Date.now() / 1000)
      }))
    };

    try {
      const response = await fetch(this.config.slackWebhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Slack API error: ${response.status}`);
      }
    } catch (error) {
      console.error('Failed to send Slack notification:', error.message);
      throw error;
    }
  }

  /**
   * Send notification to Discord
   * @private
   */
  async _sendToDiscord(message, opportunities) {
    if (!this.config.discordWebhookUrl) {
      console.warn('Discord webhook URL not configured');
      return;
    }

    const embeds = opportunities.map(opp => ({
      title: opp.title || 'Untitled Opportunity',
      description: opp.description || '',
      color: 3581519,
      fields: [
        {
          name: 'Reward',
          value: opp.reward || 'N/A',
          inline: true
        },
        {
          name: 'Platform',
          value: opp.platform || 'Unknown',
          inline: true
        },
        {
          name: 'URL',
          value: opp.url || 'N/A',
          inline: false
        }
      ],
      timestamp: new Date().toISOString(),
      footer: {
        text: 'BountyScout'
      }
    }));

    const payload = {
      content: message,
      embeds: embeds.slice(0, 10) // Discord limit
    };

    try {
      const response = await fetch(this.config.discordWebhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Discord API error: ${response.status}`);
      }
    } catch (error) {
      console.error('Failed to send Discord notification:', error.message);
      throw error;
    }
  }

  /**
   * Send email notification
   * @private
   */
  async _sendEmail(message, opportunities) {
    console.log('Email notification not yet implemented');
    // TODO: Implement email notification
  }
}

module.exports = NotificationService;
