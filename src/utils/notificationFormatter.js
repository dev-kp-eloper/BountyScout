/**
 * Formats notification messages for bounty alerts
 * @param {number} count - Number of opportunities found
 * @returns {string} Formatted notification message
 */
function formatBountyAlert(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }

  const pluralizedOpportunities = count === 1 ? 'Opportunity' : 'Opportunities';
  return `🎯 Bounty Alert: ${count} New ${pluralizedOpportunities} found`;
}

module.exports = { formatBountyAlert };
