const { correctSpelling } = require('../utils/spellcheck');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  /**
   * Formats the notification title
   * @param {number} count - Number of opportunities found
   * @returns {string} - Formatted notification title
   */
  static formatBountyAlertTitle(count) {
    if (typeof count !== 'number' || count < 0) {
      throw new Error('Count must be a non-negative number');
    }

    const pluralForm = count === 1 ? 'Opportunity' : 'Opportunities';
    const title = `🎯 Bounty Alert: ${count} New ${pluralForm} found`;
    
    return correctSpelling(title);
  }

  /**
   * Creates a notification object
   * @param {number} count - Number of opportunities
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Object} - Notification object
   */
  static createBountyNotification(count, opportunities = []) {
    if (!Array.isArray(opportunities)) {
      throw new Error('Opportunities must be an array');
    }

    return {
      title: this.formatBountyAlertTitle(count),
      count,
      opportunities,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Sends a bounty alert notification
   * @param {number} count - Number of opportunities
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Promise<Object>} - Notification result
   */
  static async sendBountyAlert(count, opportunities = []) {
    try {
      const notification = this.createBountyNotification(count, opportunities);
      
      // Log the notification (can be extended to send via email, Slack, etc.)
      console.log(`[${notification.timestamp}] ${notification.title}`);
      
      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('Error sending bounty alert:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = NotificationService;
