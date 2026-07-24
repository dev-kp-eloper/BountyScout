const { formatBountyNotification } = require('./notificationFormatter');

describe('formatBountyNotification', () => {
  test('should format single opportunity correctly', () => {
    expect(formatBountyNotification(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format multiple opportunities correctly', () => {
    expect(formatBountyNotification(13)).toBe('🎯 Bounty Alert: 13 New Opportunities found');
  });

  test('should format zero opportunities correctly', () => {
    expect(formatBountyNotification(0)).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('should handle large numbers correctly', () => {
    expect(formatBountyNotification(1000)).toBe('🎯 Bounty Alert: 1000 New Opportunities found');
  });

  test('should throw error for negative numbers', () => {
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
  });

  test('should throw error for non-number input', () => {
    expect(() => formatBountyNotification('13')).toThrow('Count must be a non-negative number');
  });

  test('should throw error for null input', () => {
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
  });

  test('should throw error for undefined input', () => {
    expect(() => formatBountyNotification(undefined)).toThrow('Count must be a non-negative number');
  });
});
