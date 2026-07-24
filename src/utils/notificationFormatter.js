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

  const pluralizedWord = count === 1 ? 'Opportunity' : 'Opportunities';
  return `🎯 Bounty Alert: ${count} New ${pluralizedWord} found`;
}

module.exports = {
  formatBountyNotification
};
