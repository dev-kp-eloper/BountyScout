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
    test('should send alert for multiple opportunities', async () => {
      const opportunities = [
        { title: 'Bug Bounty 1', reward: '$500', platform: 'HackerOne' },
        { title: 'Bug Bounty 2', reward: '$1000', platform: 'Bugcrowd' }
      ];

      const result = await service.sendBountyAlert(2, opportunities);

      expect(result.success).toBe(true);
      expect(result.title).toBe('🎯 Bounty Alert: 2 New Opportunities found');
      expect(result.count).toBe(2);
      expect(result.opportunities).toEqual(opportunities);
      expect(consoleLogSpy).toHaveBeenCalled();
    });

    test('should send alert for single opportunity', async () => {
      const opportunities = [
        { title: 'Bug Bounty 1', reward: '$500', platform: 'HackerOne' }
      ];

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

    test('should limit opportunities to 10 in notification', async () => {
      const opportunities = Array.from({ length: 15 }, (_, i) => ({
        title: `Bounty ${i + 1}`,
        reward: '$100',
        platform: 'Test'
      }));

      const result = await service.sendBountyAlert(15, opportunities);

      expect(result.success).toBe(true);
      expect(result.opportunities.length).toBe(10);
    });

    test('should handle invalid count', async () => {
      const result = await service.sendBountyAlert(-1, []);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid opportunity count');
      expect(consoleErrorSpy).toHaveBeenCalled();
    });

    test('should handle invalid opportunities array', async () => {
      const result = await service.sendBountyAlert(5, 'not an array');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Opportunities must be an array');
    });
  });

  describe('formatOpportunityList', () => {
    test('should format opportunity list correctly', () => {
      const opportunities = [
        { title: 'Bounty 1', reward: '$500', platform: 'HackerOne' },
        { title: 'Bounty 2', reward: '$1000', platform: 'Bugcrowd' }
      ];

      const result = service.formatOpportunityList(opportunities);

      expect(result).toContain('1. Bounty 1 - $500 (HackerOne)');
      expect(result).toContain('2. Bounty 2 - $1000 (Bugcrowd)');
    });

    test('should handle empty array', () => {
      const result = service.formatOpportunityList([]);
      expect(result).toBe('No opportunities to display');
    });

    test('should handle missing fields', () => {
      const opportunities = [
        { name: 'Bounty 1' },
        {}
      ];

      const result = service.formatOpportunityList(opportunities);

      expect(result).toContain('1. Bounty 1 - N/A (Unknown)');
      expect(result).toContain('2. Untitled - N/A (Unknown)');
    });
  });
});
