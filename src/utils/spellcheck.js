/**
 * Spell check utility for common typos
 */
const COMMON_TYPOS = {
  'opportunityies': 'opportunities',
  'oppurtunities': 'opportunities',
  'oportunities': 'opportunities'
};

/**
 * Corrects common spelling mistakes
 * @param {string} text - Text to check and correct
 * @returns {string} - Corrected text
 */
function correctSpelling(text) {
  if (!text || typeof text !== 'string') {
    return text;
  }

  let correctedText = text;
  
  Object.keys(COMMON_TYPOS).forEach(typo => {
    const correction = COMMON_TYPOS[typo];
    const regex = new RegExp(typo, 'gi');
    correctedText = correctedText.replace(regex, (match) => {
      // Preserve case
      if (match[0] === match[0].toUpperCase()) {
        return correction.charAt(0).toUpperCase() + correction.slice(1);
      }
      return correction;
    });
  });

  return correctedText;
}

module.exports = {
  correctSpelling,
  COMMON_TYPOS
};
