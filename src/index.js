const { formatBountyNotification } = require('./utils/notificationFormatter');
const { sendBountyNotification } = require('./services/notificationService');

module.exports = {
  formatBountyNotification,
  sendBountyNotification
};
