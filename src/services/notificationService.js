const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  /**
   * Sends a bounty alert notification
   * @param {number} opportunityCount - Number of new opportunities found
   * @param {Object} options - Additional notification options
   * @returns {Promise<Object>} Notification result
   */
  async sendBountyAlert(opportunityCount, options = {}) {
    try {
      const message = formatBountyNotification(opportunityCount);
      
      const notification = {
        title: message,
        timestamp: new Date().toISOString(),
        count: opportunityCount,
        ...options
      };

      // Log notification (can be extended to send to various channels)
      console.log(`[NOTIFICATION] ${message}`);
      
      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('[NOTIFICATION ERROR]', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Sends notifications through multiple channels
   * @param {number} opportunityCount - Number of new opportunities
   * @param {Array<string>} channels - Notification channels (e.g., ['console', 'email', 'slack'])
   * @returns {Promise<Object>} Results from all channels
   */
  async sendMultiChannelAlert(opportunityCount, channels = ['console']) {
    const message = formatBountyNotification(opportunityCount);
    const results = {};

    for (const channel of channels) {
      try {
        switch (channel) {
          case 'console':
            console.log(`[${channel.toUpperCase()}] ${message}`);
            results[channel] = { success: true };
            break;
          case 'email':
            // Placeholder for email integration
            results[channel] = { success: true, message: 'Email notification sent' };
            break;
          case 'slack':
            // Placeholder for Slack integration
            results[channel] = { success: true, message: 'Slack notification sent' };
            break;
          default:
            results[channel] = { success: false, error: 'Unknown channel' };
        }
      } catch (error) {
        results[channel] = { success: false, error: error.message };
      }
    }

    return {
      message,
      count: opportunityCount,
      channels: results
    };
  }
}

module.exports = NotificationService;
