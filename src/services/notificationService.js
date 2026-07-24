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
      
      // Log the notification
      console.log(message);
      
      // Additional notification logic can be added here
      // (e.g., sending to Slack, Discord, email, etc.)
      
      return {
        success: true,
        message,
        count: opportunityCount,
        timestamp: new Date().toISOString()
      };
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
   * Formats opportunity details for notification
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {string} Formatted opportunity details
   */
  formatOpportunityDetails(opportunities) {
    if (!Array.isArray(opportunities) || opportunities.length === 0) {
      return 'No opportunities to display';
    }

    return opportunities.map((opp, index) => {
      const title = opp.title || 'Untitled';
      const reward = opp.reward || 'N/A';
      const url = opp.url || '#';
      return `${index + 1}. ${title} - Reward: ${reward}\n   ${url}`;
    }).join('\n\n');
  }
}

module.exports = NotificationService;
