const { formatBountyAlert } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  constructor() {
    this.subscribers = [];
  }

  /**
   * Subscribe to notifications
   * @param {Function} callback - Callback function to handle notifications
   */
  subscribe(callback) {
    if (typeof callback !== 'function') {
      throw new Error('Callback must be a function');
    }
    this.subscribers.push(callback);
  }

  /**
   * Unsubscribe from notifications
   * @param {Function} callback - Callback function to remove
   */
  unsubscribe(callback) {
    this.subscribers = this.subscribers.filter(sub => sub !== callback);
  }

  /**
   * Send bounty alert notification
   * @param {number} count - Number of new opportunities
   * @param {Array} opportunities - Array of opportunity objects
   */
  sendBountyAlert(count, opportunities = []) {
    try {
      const message = formatBountyAlert(count);
      const notification = {
        message,
        count,
        opportunities,
        timestamp: new Date().toISOString()
      };

      this.subscribers.forEach(callback => {
        try {
          callback(notification);
        } catch (error) {
          console.error('Error in notification subscriber:', error);
        }
      });

      return notification;
    } catch (error) {
      console.error('Error sending bounty alert:', error);
      throw error;
    }
  }
}

module.exports = NotificationService;
