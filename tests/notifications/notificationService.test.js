const NotificationService = require('../../src/notifications/notificationService');

describe('NotificationService', () => {
  describe('generateBountyAlert', () => {
    test('should generate correct message for singular opportunity', () => {
      const result = NotificationService.generateBountyAlert(1);
      expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should generate correct message for multiple opportunities', () => {
      const result = NotificationService.generateBountyAlert(13);
      expect(result).toBe('🎯 Bounty Alert: 13 New Opportunities found');
    });

    test('should generate correct message for zero opportunities', () => {
      const result = NotificationService.generateBountyAlert(0);
      expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
    });

    test('should throw error for invalid count', () => {
      expect(() => NotificationService.generateBountyAlert('invalid')).toThrow();
      expect(() => NotificationService.generateBountyAlert(-1)).toThrow();
    });
  });

  describe('sendBountyAlert', () => {
    test('should send alert successfully', async () => {
      const result = await NotificationService.sendBountyAlert(13);
      expect(result.success).toBe(true);
      expect(result.message).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.count).toBe(13);
      expect(result.timestamp).toBeDefined();
    });

    test('should handle errors gracefully', async () => {
      const result = await NotificationService.sendBountyAlert('invalid');
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  describe('fixNotificationMessage', () => {
    test('should fix typos in notification messages', () => {
      const input = '🎯 Bounty Alert: 13 New Opportunityies found';
      const expected = '🎯 Bounty Alert: 13 New Opportunities found';
      const result = NotificationService.fixNotificationMessage(input);
      expect(result).toBe(expected);
    });
  });
});
