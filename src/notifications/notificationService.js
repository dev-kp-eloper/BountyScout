const { fixTypos, pluralize } = require('../utils/textFormatter');

/**
 * Notification service for bounty alerts
 */
class NotificationService {
  /**
   * Generates a bounty alert message
   * @param {number} count - Number of opportunities found
   * @returns {string} - Formatted alert message
   */
  static generateBountyAlert(count) {
    if (typeof count !== 'number' || count < 0) {
      throw new Error('Count must be a non-negative number');
    }

    const word = count === 1 ? 'Opportunity' : 'Opportunities';
    return `🎯 Bounty Alert: ${count} New ${word} found`;
  }

  /**
   * Sends a bounty alert notification
   * @param {number} count - Number of opportunities found
   * @param {Object} options - Additional options for the notification
   * @returns {Object} - Notification result
   */
  static async sendBountyAlert(count, options = {}) {
    try {
      const message = this.generateBountyAlert(count);
      
      // Log the notification
      console.log(message);
      
      return {
        success: true,
        message,
        count,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error sending bounty alert:', error);
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Fixes typos in existing notification messages
   * @param {string} message - The message to fix
   * @returns {string} - The corrected message
   */
  static fixNotificationMessage(message) {
    return fixTypos(message);
  }
}

module.exports = NotificationService;
