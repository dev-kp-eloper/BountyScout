/**
 * Formats notification messages for bounty alerts
 * @param {number} count - Number of new opportunities
 * @returns {string} Formatted notification message
 */
function formatBountyNotification(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }

  if (count === 0) {
    return '🎯 Bounty Alert: No new opportunities found';
  }

  const pluralSuffix = count === 1 ? 'y' : 'ies';
  return `🎯 Bounty Alert: ${count} New Opportunit${pluralSuffix} found`;
}

module.exports = {
  formatBountyNotification
};
