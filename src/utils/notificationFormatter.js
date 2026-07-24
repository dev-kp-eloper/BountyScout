/**
 * Formats notification messages for bounty alerts
 * @param {number} count - Number of new opportunities
 * @returns {string} Formatted notification message
 */
function formatBountyAlert(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }
  
  const pluralizedWord = count === 1 ? 'Opportunity' : 'Opportunities';
  return `🎯 Bounty Alert: ${count} New ${pluralizedWord} found`;
}

module.exports = { formatBountyAlert };
