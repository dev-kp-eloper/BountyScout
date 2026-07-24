const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification Service for handling bounty alerts
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
      if (typeof opportunityCount !== 'number' || opportunityCount < 0) {
        throw new Error('Invalid opportunity count');
      }

      const message = formatBountyNotification(opportunityCount);
      
      const notification = {
        message,
        timestamp: new Date().toISOString(),
        count: opportunityCount,
        type: 'bounty_alert',
        ...options
      };

      // Log the notification
      console.log(`[NotificationService] ${message}`);

      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('[NotificationService] Error sending bounty alert:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Sends multiple bounty alerts in batch
   * @param {Array<number>} counts - Array of opportunity counts
   * @returns {Promise<Array<Object>>} Array of notification results
   */
  async sendBatchAlerts(counts) {
    if (!Array.isArray(counts)) {
      throw new Error('Counts must be an array');
    }

    const results = [];
    for (const count of counts) {
      const result = await this.sendBountyAlert(count);
      results.push(result);
    }

    return results;
  }
}

module.exports = NotificationService;
