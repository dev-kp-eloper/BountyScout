/**
 * Text formatting utilities
 */

/**
 * Fixes common typos in text
 * @param {string} text - The text to fix
 * @returns {string} - The corrected text
 */
function fixTypos(text) {
  if (!text || typeof text !== 'string') {
    return text;
  }

  const typoMap = {
    'Opportunityies': 'Opportunities',
    'opportunityies': 'opportunities',
    'Opportunitiy': 'Opportunity',
    'opportunitiy': 'opportunity'
  };

  let correctedText = text;
  
  for (const [typo, correction] of Object.entries(typoMap)) {
    const regex = new RegExp(typo, 'g');
    correctedText = correctedText.replace(regex, correction);
  }

  return correctedText;
}

/**
 * Pluralizes a word correctly
 * @param {string} word - The word to pluralize
 * @param {number} count - The count to determine pluralization
 * @returns {string} - The correctly pluralized word
 */
function pluralize(word, count) {
  if (!word || typeof word !== 'string') {
    return word;
  }

  if (count === 1) {
    return word;
  }

  // Handle special cases
  const specialCases = {
    'opportunity': 'opportunities',
    'Opportunity': 'Opportunities'
  };

  return specialCases[word] || `${word}s`;
}

module.exports = {
  fixTypos,
  pluralize
};
