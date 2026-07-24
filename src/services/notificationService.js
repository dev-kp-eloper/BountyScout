const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  /**
   * Sends a bounty alert notification
   * @param {number} opportunityCount - Number of new opportunities found
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Object} Notification result
   */
  async sendBountyAlert(opportunityCount, opportunities = []) {
    try {
      if (typeof opportunityCount !== 'number' || opportunityCount < 0) {
        throw new Error('Invalid opportunity count');
      }

      if (!Array.isArray(opportunities)) {
        throw new Error('Opportunities must be an array');
      }

      const message = formatBountyNotification(opportunityCount);
      
      const notification = {
        title: message,
        timestamp: new Date().toISOString(),
        count: opportunityCount,
        opportunities: opportunities.slice(0, 10), // Limit to first 10 for notification
        success: true
      };

      // Log the notification
      console.log(`[${notification.timestamp}] ${message}`);
      
      if (opportunityCount > 0 && opportunities.length > 0) {
        console.log(`Top opportunities:`);
        opportunities.slice(0, 5).forEach((opp, index) => {
          console.log(`  ${index + 1}. ${opp.title || opp.name || 'Untitled'} - ${opp.reward || 'N/A'}`);
        });
      }

      return notification;
    } catch (error) {
      console.error('Error sending bounty alert:', error.message);
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Formats and sends multiple bounty alerts
   * @param {Array} alerts - Array of alert objects with count and opportunities
   * @returns {Array} Array of notification results
   */
  async sendBulkAlerts(alerts) {
    if (!Array.isArray(alerts)) {
      throw new Error('Alerts must be an array');
    }

    const results = [];
    for (const alert of alerts) {
      const result = await this.sendBountyAlert(
        alert.count || 0,
        alert.opportunities || []
      );
      results.push(result);
    }

    return results;
  }
}

module.exports = NotificationService;
