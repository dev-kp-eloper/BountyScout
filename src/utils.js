function deduplicateBounties(bounties) {
  const seen = new Map();
  
  for (const bounty of bounties) {
    if (!seen.has(bounty.id)) {
      seen.set(bounty.id, bounty);
    }
  }
  
  return Array.from(seen.values());
}

function filterBounties(bounties) {
  return bounties.filter(bounty => {
    const titleLower = bounty.title.toLowerCase();
    const bodyLower = (bounty.body || '').toLowerCase();
    const combined = titleLower + ' ' + bodyLower;
    
    // Check for bounty indicators
    const hasBountyKeyword = (
      combined.includes('bounty') ||
      combined.includes('reward') ||
      combined.includes('prize') ||
      combined.includes('$') ||
      combined.includes('usd') ||
      combined.includes('eur') ||
      combined.includes('compensation') ||
      combined.includes('paid')
    );
    
    // Check for bounty labels
    const hasBountyLabel = bounty.labels.some(label => {
      const labelLower = label.toLowerCase();
      return (
        labelLower.includes('bounty') ||
        labelLower.includes('reward') ||
        labelLower.includes('prize') ||
        labelLower.includes('paid') ||
        labelLower.includes('compensation')
      );
    });
    
    // Exclude spam/irrelevant issues
    const isSpam = (
      titleLower.includes('test') && titleLower.length < 20 ||
      titleLower.includes('spam') ||
      combined.includes('do not merge')
    );
    
    return (hasBountyKeyword || hasBountyLabel) && !isSpam;
  });
}

function extractBountyAmount(text) {
  if (!text) return null;
  
  const patterns = [
    /\$([0-9,]+(?:\.[0-9]{2})?)/,
    /([0-9,]+)\s*USD/i,
    /([0-9,]+)\s*EUR/i,
    /([0-9,]+)\s*dollars?/i
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1].replace(/,/g, '');
    }
  }
  
  return null;
}

module.exports = {
  deduplicateBounties,
  filterBounties,
  extractBountyAmount
};
