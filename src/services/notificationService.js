const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  constructor(config = {}) {
    this.config = config;
    this.notificationHandlers = [];
  }

  /**
   * Register a notification handler
   * @param {Function} handler - Function to handle notifications
   */
  registerHandler(handler) {
    if (typeof handler !== 'function') {
      throw new Error('Handler must be a function');
    }
    this.notificationHandlers.push(handler);
  }

  /**
   * Send bounty alert notification
   * @param {number} count - Number of new opportunities
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Promise<void>}
   */
  async sendBountyAlert(count, opportunities = []) {
    try {
      const message = formatBountyNotification(count);
      
      const notificationData = {
        message,
        count,
        opportunities,
        timestamp: new Date().toISOString()
      };

      // Send notification through all registered handlers
      const promises = this.notificationHandlers.map(handler => 
        Promise.resolve(handler(notificationData))
      );

      await Promise.allSettled(promises);
      
      return notificationData;
    } catch (error) {
      console.error('Error sending bounty alert:', error);
      throw error;
    }
  }

  /**
   * Clear all notification handlers
   */
  clearHandlers() {
    this.notificationHandlers = [];
  }
}

module.exports = NotificationService;
