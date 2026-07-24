const NotificationService = require('../notificationService');

describe('NotificationService', () => {
  let service;
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    service = new NotificationService();
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('sendBountyAlert', () => {
    test('should send notification with correct message for 13 opportunities', async () => {
      const result = await service.sendBountyAlert(13);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.notification.type).toBe('bounty_alert');
      expect(result.notification.count).toBe(13);
      expect(result.notification.timestamp).toBeDefined();
      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[NotificationService] 🎯 Bounty Alert: 13 New Opportunities found'
      );
    });

    test('should send notification with correct message for 1 opportunity', async () => {
      const result = await service.sendBountyAlert(1);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should include additional options in notification', async () => {
      const options = {
        priority: 'high',
        category: 'web3'
      };
      const result = await service.sendBountyAlert(5, options);

      expect(result.success).toBe(true);
      expect(result.notification.priority).toBe('high');
      expect(result.notification.category).toBe('web3');
    });

    test('should handle errors gracefully', async () => {
      const result = await service.sendBountyAlert(-1);

      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(consoleErrorSpy).toHaveBeenCalled();
    });
  });

  describe('sendBatchAlerts', () => {
    test('should send multiple alerts', async () => {
      const alerts = [
        { count: 13, options: { category: 'web3' } },
        { count: 5, options: { category: 'mobile' } },
        { count: 1, options: { category: 'backend' } }
      ];

      const results = await service.sendBatchAlerts(alerts);

      expect(results).toHaveLength(3);
      expect(results[0].success).toBe(true);
      expect(results[0].notification.count).toBe(13);
      expect(results[1].notification.count).toBe(5);
      expect(results[2].notification.count).toBe(1);
    });

    test('should throw error for invalid input', async () => {
      await expect(service.sendBatchAlerts('not an array')).rejects.toThrow(
        'Alerts must be an array'
      );
    });

    test('should handle empty array', async () => {
      const results = await service.sendBatchAlerts([]);
      expect(results).toHaveLength(0);
    });
  });
});
