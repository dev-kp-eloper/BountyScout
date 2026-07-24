const { formatBountyNotification } = require('./notificationFormatter');

describe('formatBountyNotification', () => {
  test('formats single opportunity correctly', () => {
    expect(formatBountyNotification(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('formats multiple opportunities correctly', () => {
    expect(formatBountyNotification(13)).toBe('🎯 Bounty Alert: 13 New Opportunities found');
    expect(formatBountyNotification(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatBountyNotification(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('handles zero opportunities', () => {
    expect(formatBountyNotification(0)).toBe('🎯 Bounty Alert: No new opportunities found');
  });

  test('throws error for invalid input', () => {
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification('13')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(undefined)).toThrow('Count must be a non-negative number');
  });
});
