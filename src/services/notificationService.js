const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  /**
   * Send a bounty alert notification
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
        type: 'bounty_alert',
        count: opportunityCount,
        ...options
      };

      // Log notification (can be extended to send to external services)
      console.log(`[NotificationService] ${message}`);
      
      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('[NotificationService] Error sending bounty alert:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Send batch notifications for multiple bounty alerts
   * @param {Array<Object>} alerts - Array of alert objects with count and options
   * @returns {Promise<Array<Object>>} Array of notification results
   */
  async sendBatchAlerts(alerts) {
    if (!Array.isArray(alerts)) {
      throw new Error('Alerts must be an array');
    }

    const results = [];
    for (const alert of alerts) {
      const result = await this.sendBountyAlert(alert.count, alert.options);
      results.push(result);
    }

    return results;
  }
}

module.exports = NotificationService;
