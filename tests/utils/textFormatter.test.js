const { fixTypos, pluralize } = require('../../src/utils/textFormatter');

describe('textFormatter', () => {
  describe('fixTypos', () => {
    test('should fix "Opportunityies" to "Opportunities"', () => {
      const input = '🎯 Bounty Alert: 13 New Opportunityies found';
      const expected = '🎯 Bounty Alert: 13 New Opportunities found';
      expect(fixTypos(input)).toBe(expected);
    });

    test('should fix lowercase "opportunityies" to "opportunities"', () => {
      const input = 'Found 5 new opportunityies';
      const expected = 'Found 5 new opportunities';
      expect(fixTypos(input)).toBe(expected);
    });

    test('should fix "Opportunitiy" to "Opportunity"', () => {
      const input = '1 New Opportunitiy found';
      const expected = '1 New Opportunity found';
      expect(fixTypos(input)).toBe(expected);
    });

    test('should handle null or undefined input', () => {
      expect(fixTypos(null)).toBe(null);
      expect(fixTypos(undefined)).toBe(undefined);
    });

    test('should handle non-string input', () => {
      expect(fixTypos(123)).toBe(123);
      expect(fixTypos({})).toEqual({});
    });

    test('should handle text without typos', () => {
      const input = '🎯 Bounty Alert: 13 New Opportunities found';
      expect(fixTypos(input)).toBe(input);
    });
  });

  describe('pluralize', () => {
    test('should return singular form for count of 1', () => {
      expect(pluralize('opportunity', 1)).toBe('opportunity');
      expect(pluralize('Opportunity', 1)).toBe('Opportunity');
    });

    test('should return plural form for count greater than 1', () => {
      expect(pluralize('opportunity', 2)).toBe('opportunities');
      expect(pluralize('Opportunity', 13)).toBe('Opportunities');
    });

    test('should return plural form for count of 0', () => {
      expect(pluralize('opportunity', 0)).toBe('opportunities');
    });

    test('should handle null or undefined input', () => {
      expect(pluralize(null, 5)).toBe(null);
      expect(pluralize(undefined, 5)).toBe(undefined);
    });
  });
});
