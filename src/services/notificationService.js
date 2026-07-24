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

      // Log the notification (can be extended to send to external services)
      console.log(`[${notification.timestamp}] ${notification.title}`);
      
      if (opportunityCount > 0 && opportunities.length > 0) {
        console.log(`Preview: ${opportunities.slice(0, 3).map(o => o.title || o.name || 'Untitled').join(', ')}`);
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
   * Formats opportunity details for display
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {string} Formatted opportunity list
   */
  formatOpportunityList(opportunities) {
    if (!Array.isArray(opportunities) || opportunities.length === 0) {
      return 'No opportunities to display';
    }

    return opportunities.map((opp, index) => {
      const title = opp.title || opp.name || 'Untitled';
      const reward = opp.reward || opp.bounty || 'N/A';
      const platform = opp.platform || 'Unknown';
      return `${index + 1}. ${title} - ${reward} (${platform})`;
    }).join('\n');
  }
}

module.exports = NotificationService;
