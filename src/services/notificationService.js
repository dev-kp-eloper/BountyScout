const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends bounty notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Object} options - Notification options
 */
async function sendBountyNotification(opportunityCount, options = {}) {
  try {
    const message = formatBountyNotification(opportunityCount);
    
    // Log the notification
    console.log(message);
    
    // Send notification through configured channels
    if (options.channels) {
      for (const channel of options.channels) {
        await channel.send(message);
      }
    }
    
    return {
      success: true,
      message
    };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendBountyNotification
};
