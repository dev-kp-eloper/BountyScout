const NotificationService = require('../../src/notifications/notificationService');

describe('NotificationService', () => {
  describe('formatBountyAlertTitle', () => {
    test('should format title correctly for single opportunity', () => {
      const title = NotificationService.formatBountyAlertTitle(1);
      expect(title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should format title correctly for multiple opportunities', () => {
      const title = NotificationService.formatBountyAlertTitle(13);
      expect(title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
    });

    test('should format title correctly for zero opportunities', () => {
      const title = NotificationService.formatBountyAlertTitle(0);
      expect(title).toBe('🎯 Bounty Alert: 0 New Opportunities found');
    });

    test('should throw error for invalid count', () => {
      expect(() => NotificationService.formatBountyAlertTitle('invalid'))
        .toThrow('Count must be a non-negative number');
    });

    test('should throw error for negative count', () => {
      expect(() => NotificationService.formatBountyAlertTitle(-1))
        .toThrow('Count must be a non-negative number');
    });
  });

  describe('createBountyNotification', () => {
    test('should create notification object with correct structure', () => {
      const opportunities = [{ id: 1, title: 'Test Bounty' }];
      const notification = NotificationService.createBountyNotification(1, opportunities);

      expect(notification).toHaveProperty('title');
      expect(notification).toHaveProperty('count');
      expect(notification).toHaveProperty('opportunities');
      expect(notification).toHaveProperty('timestamp');
      expect(notification.count).toBe(1);
      expect(notification.opportunities).toEqual(opportunities);
    });

    test('should handle empty opportunities array', () => {
      const notification = NotificationService.createBountyNotification(0, []);
      expect(notification.opportunities).toEqual([]);
      expect(notification.count).toBe(0);
    });

    test('should throw error for non-array opportunities', () => {
      expect(() => NotificationService.createBountyNotification(1, 'invalid'))
        .toThrow('Opportunities must be an array');
    });
  });

  describe('sendBountyAlert', () => {
    let consoleLogSpy;
    let consoleErrorSpy;

    beforeEach(() => {
      consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
      consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    });

    afterEach(() => {
      consoleLogSpy.mockRestore();
      consoleErrorSpy.mockRestore();
    });

    test('should send bounty alert successfully', async () => {
      const opportunities = [{ id: 1, title: 'Test Bounty' }];
      const result = await NotificationService.sendBountyAlert(1, opportunities);

      expect(result.success).toBe(true);
      expect(result.notification).toBeDefined();
      expect(consoleLogSpy).toHaveBeenCalled();
    });

    test('should handle errors gracefully', async () => {
      const result = await NotificationService.sendBountyAlert(1, 'invalid');

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(consoleErrorSpy).toHaveBeenCalled();
    });
  });
});
