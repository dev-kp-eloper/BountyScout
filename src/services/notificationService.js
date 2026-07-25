const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  /**
   * Sends a bounty alert notification
   * @param {number} opportunityCount - Number of new opportunities found
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Promise<Object>} Notification result
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
        hasMore: opportunities.length > 10
      };

      // Log the notification (can be extended to send to external services)
      console.log(`[${notification.timestamp}] ${notification.title}`);
      
      if (opportunityCount > 0) {
        console.log(`Details: ${opportunities.length} opportunities available`);
      }

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

  /**
   * Formats opportunity details for display
   * @param {Object} opportunity - Opportunity object
   * @returns {string} Formatted opportunity string
   */
  formatOpportunityDetails(opportunity) {
    if (!opportunity || typeof opportunity !== 'object') {
      return 'Invalid opportunity';
    }

    const title = opportunity.title || 'Untitled';
    const reward = opportunity.reward || 'N/A';
    const platform = opportunity.platform || 'Unknown';
    
    return `${title} - ${reward} (${platform})`;
  }
}

module.exports = NotificationService;
