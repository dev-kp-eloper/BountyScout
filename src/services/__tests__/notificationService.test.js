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
    test('should send alert for 13 opportunities', async () => {
      const opportunities = Array.from({ length: 13 }, (_, i) => ({
        title: `Bounty ${i + 1}`,
        reward: `$${(i + 1) * 100}`
      }));

      const result = await service.sendBountyAlert(13, opportunities);

      expect(result.success).toBe(true);
      expect(result.title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.count).toBe(13);
      expect(result.opportunities).toHaveLength(10); // Limited to 10
      expect(result.timestamp).toBeDefined();
    });

    test('should send alert for single opportunity', async () => {
      const opportunities = [{ title: 'Bug Fix', reward: '$500' }];

      const result = await service.sendBountyAlert(1, opportunities);

      expect(result.success).toBe(true);
      expect(result.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
      expect(result.count).toBe(1);
    });

    test('should handle zero opportunities', async () => {
      const result = await service.sendBountyAlert(0, []);

      expect(result.success).toBe(true);
      expect(result.title).toBe('🎯 Bounty Alert: No new opportunities found');
      expect(result.count).toBe(0);
    });

    test('should handle invalid count', async () => {
      const result = await service.sendBountyAlert(-1, []);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid opportunity count');
    });

    test('should handle invalid opportunities array', async () => {
      const result = await service.sendBountyAlert(5, 'not an array');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Opportunities must be an array');
    });

    test('should log top opportunities', async () => {
      const opportunities = [
        { title: 'Bounty 1', reward: '$100' },
        { title: 'Bounty 2', reward: '$200' },
        { title: 'Bounty 3', reward: '$300' }
      ];

      await service.sendBountyAlert(3, opportunities);

      expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('🎯 Bounty Alert: 3 New Opportunities found'));
      expect(consoleLogSpy).toHaveBeenCalledWith('Top opportunities:');
    });
  });

  describe('sendBulkAlerts', () => {
    test('should send multiple alerts', async () => {
      const alerts = [
        { count: 5, opportunities: [{ title: 'Test 1' }] },
        { count: 3, opportunities: [{ title: 'Test 2' }] }
      ];

      const results = await service.sendBulkAlerts(alerts);

      expect(results).toHaveLength(2);
      expect(results[0].success).toBe(true);
      expect(results[0].count).toBe(5);
      expect(results[1].success).toBe(true);
      expect(results[1].count).toBe(3);
    });

    test('should throw error for invalid input', async () => {
      await expect(service.sendBulkAlerts('not an array')).rejects.toThrow('Alerts must be an array');
    });
  });
});
