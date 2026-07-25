const { formatBountyAlert } = require('./notificationFormatter');

describe('formatBountyAlert', () => {
  test('formats single opportunity correctly', () => {
    expect(formatBountyAlert(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('formats multiple opportunities correctly', () => {
    expect(formatBountyAlert(19)).toBe('🎯 Bounty Alert: 19 New Opportunities found');
  });

  test('formats zero opportunities correctly', () => {
    expect(formatBountyAlert(0)).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('throws error for negative numbers', () => {
    expect(() => formatBountyAlert(-1)).toThrow('Count must be a non-negative number');
  });

  test('throws error for non-number input', () => {
    expect(() => formatBountyAlert('19')).toThrow('Count must be a non-negative number');
  });

  test('throws error for null input', () => {
    expect(() => formatBountyAlert(null)).toThrow('Count must be a non-negative number');
  });
});
