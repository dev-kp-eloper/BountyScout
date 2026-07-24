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
    test('sends notification for valid count', async () => {
      const result = await service.sendBountyAlert(13);
      
      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.notification.count).toBe(13);
      expect(result.notification.timestamp).toBeDefined();
      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[NOTIFICATION] 🎯 Bounty Alert: 13 New Opportunities found'
      );
    });

    test('includes additional options in notification', async () => {
      const options = { priority: 'high', url: 'https://example.com' };
      const result = await service.sendBountyAlert(5, options);
      
      expect(result.success).toBe(true);
      expect(result.notification.priority).toBe('high');
      expect(result.notification.url).toBe('https://example.com');
    });

    test('handles errors gracefully', async () => {
      const result = await service.sendBountyAlert('invalid');
      
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(consoleErrorSpy).toHaveBeenCalled();
    });
  });

  describe('sendMultiChannelAlert', () => {
    test('sends notification to console channel', async () => {
      const result = await service.sendMultiChannelAlert(13, ['console']);
      
      expect(result.message).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.count).toBe(13);
      expect(result.channels.console.success).toBe(true);
    });

    test('sends notification to multiple channels', async () => {
      const result = await service.sendMultiChannelAlert(13, ['console', 'email', 'slack']);
      
      expect(result.channels.console.success).toBe(true);
      expect(result.channels.email.success).toBe(true);
      expect(result.channels.slack.success).toBe(true);
    });

    test('handles unknown channels', async () => {
      const result = await service.sendMultiChannelAlert(13, ['unknown']);
      
      expect(result.channels.unknown.success).toBe(false);
      expect(result.channels.unknown.error).toBe('Unknown channel');
    });
  });
});
