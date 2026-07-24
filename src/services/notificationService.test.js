const NotificationService = require('./notificationService');
const { formatBountyNotification } = require('../utils/notificationFormatter');

jest.mock('../utils/notificationFormatter');

describe('NotificationService', () => {
  let service;
  let consoleLogSpy;
  let consoleWarnSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    formatBountyNotification.mockReturnValue('🎯 Bounty Alert: 13 New Opportunities found');
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleWarnSpy.mockRestore();
    consoleErrorSpy.mockRestore();
    jest.clearAllMocks();
  });

  describe('constructor', () => {
    test('should initialize with default config', () => {
      service = new NotificationService();
      expect(service.config.enabled).toBe(true);
      expect(service.config.channels).toEqual(['console']);
    });

    test('should initialize with custom config', () => {
      service = new NotificationService({
        enabled: false,
        channels: ['slack', 'discord']
      });
      expect(service.config.enabled).toBe(false);
      expect(service.config.channels).toEqual(['slack', 'discord']);
    });
  });

  describe('sendBountyAlert', () => {
    test('should send notification to console channel', async () => {
      service = new NotificationService();
      await service.sendBountyAlert(13, []);
      
      expect(formatBountyNotification).toHaveBeenCalledWith(13);
      expect(consoleLogSpy).toHaveBeenCalledWith('🎯 Bounty Alert: 13 New Opportunities found');
    });

    test('should not send notification when disabled', async () => {
      service = new NotificationService({ enabled: false });
      await service.sendBountyAlert(13, []);
      
      expect(formatBountyNotification).not.toHaveBeenCalled();
      expect(consoleLogSpy).not.toHaveBeenCalled();
    });

    test('should log opportunities when provided', async () => {
      service = new NotificationService();
      const opportunities = [
        { title: 'Bug Bounty 1', reward: '$500' },
        { title: 'Bug Bounty 2', reward: '$1000' }
      ];
      
      await service.sendBountyAlert(2, opportunities);
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Opportunities:', opportunities);
    });

    test('should handle errors gracefully', async () => {
      service = new NotificationService();
      formatBountyNotification.mockImplementation(() => {
        throw new Error('Formatting error');
      });

      await expect(service.sendBountyAlert(13, [])).rejects.toThrow('Formatting error');
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error sending bounty alert:', 'Formatting error');
    });

    test('should warn about unknown channels', async () => {
      service = new NotificationService({ channels: ['unknown'] });
      await service.sendBountyAlert(13, []);
      
      expect(consoleWarnSpy).toHaveBeenCalledWith('Unknown notification channel: unknown');
    });
  });

  describe('Slack integration', () => {
    test('should warn when Slack webhook URL is not configured', async () => {
      service = new NotificationService({ channels: ['slack'] });
      await service.sendBountyAlert(13, []);
      
      expect(consoleWarnSpy).toHaveBeenCalledWith('Slack webhook URL not configured');
    });
  });

  describe('Discord integration', () => {
    test('should warn when Discord webhook URL is not configured', async () => {
      service = new NotificationService({ channels: ['discord'] });
      await service.sendBountyAlert(13, []);
      
      expect(consoleWarnSpy).toHaveBeenCalledWith('Discord webhook URL not configured');
    });
  });
});
