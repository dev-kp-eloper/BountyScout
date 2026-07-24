const { correctSpelling, COMMON_TYPOS } = require('../../src/utils/spellcheck');

describe('Spellcheck Utility', () => {
  describe('correctSpelling', () => {
    test('should correct "opportunityies" to "opportunities"', () => {
      const input = '13 New Opportunityies found';
      const expected = '13 New Opportunities found';
      expect(correctSpelling(input)).toBe(expected);
    });

    test('should correct lowercase typos', () => {
      const input = 'opportunityies';
      const expected = 'opportunities';
      expect(correctSpelling(input)).toBe(expected);
    });

    test('should preserve case for capitalized words', () => {
      const input = 'Opportunityies';
      const expected = 'Opportunities';
      expect(correctSpelling(input)).toBe(expected);
    });

    test('should handle multiple typos in one string', () => {
      const input = 'opportunityies and oppurtunities';
      const expected = 'opportunities and opportunities';
      expect(correctSpelling(input)).toBe(expected);
    });

    test('should return unchanged text if no typos found', () => {
      const input = 'opportunities';
      expect(correctSpelling(input)).toBe(input);
    });

    test('should handle null or undefined input', () => {
      expect(correctSpelling(null)).toBe(null);
      expect(correctSpelling(undefined)).toBe(undefined);
    });

    test('should handle non-string input', () => {
      expect(correctSpelling(123)).toBe(123);
      expect(correctSpelling({})).toEqual({});
    });

    test('should handle empty string', () => {
      expect(correctSpelling('')).toBe('');
    });
  });

  describe('COMMON_TYPOS', () => {
    test('should contain expected typo mappings', () => {
      expect(COMMON_TYPOS).toHaveProperty('opportunityies');
      expect(COMMON_TYPOS.opportunityies).toBe('opportunities');
    });
  });
});
