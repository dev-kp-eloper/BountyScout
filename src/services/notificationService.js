const { formatBountyAlert } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Object} options - Notification options
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(opportunityCount, options = {}) {
  try {
    if (typeof opportunityCount !== 'number' || opportunityCount < 0) {
      throw new Error('Invalid opportunity count');
    }

    const message = formatBountyAlert(opportunityCount);
    
    // Log the notification
    console.log(`[${new Date().toISOString()}] ${message}`);

    // Return notification details
    return {
      success: true,
      message,
      count: opportunityCount,
      timestamp: new Date().toISOString(),
      ...options
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

module.exports = { sendBountyAlert };
