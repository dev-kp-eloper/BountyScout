const { formatBountyAlert } = require('./notificationFormatter');

describe('formatBountyAlert', () => {
  test('should format singular opportunity correctly', () => {
    expect(formatBountyAlert(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format plural opportunities correctly', () => {
    expect(formatBountyAlert(13)).toBe('🎯 Bounty Alert: 13 New Opportunities found');
    expect(formatBountyAlert(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatBountyAlert(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    expect(formatBountyAlert(0)).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('should throw error for invalid input', () => {
    expect(() => formatBountyAlert(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlert('13')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlert(null)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlert(undefined)).toThrow('Count must be a non-negative number');
  });
});
