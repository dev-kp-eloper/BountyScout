const { formatBountyNotification } = require('../notificationFormatter');

describe('formatBountyNotification', () => {
  test('should format singular opportunity correctly', () => {
    expect(formatBountyNotification(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format plural opportunities correctly', () => {
    expect(formatBountyNotification(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatBountyNotification(13)).toBe('🎯 Bounty Alert: 13 New Opportunities found');
    expect(formatBountyNotification(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    expect(formatBountyNotification(0)).toBe('🎯 Bounty Alert: No new opportunities found');
  });

  test('should throw error for invalid input', () => {
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification('13')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(undefined)).toThrow('Count must be a non-negative number');
  });
});
