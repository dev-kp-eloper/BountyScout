const NotificationService = require('../notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  describe('sendBountyAlert', () => {
    test('should send notification for multiple opportunities', async () => {
      const opportunities = [
        { title: 'Bug Bounty 1', reward: 500, platform: 'HackerOne' },
        { title: 'Bug Bounty 2', reward: 1000, platform: 'Bugcrowd' }
      ];

      const result = await service.sendBountyAlert(13, opportunities);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.notification.count).toBe(13);
      expect(result.notification.opportunities).toEqual(opportunities);
      expect(console.log).toHaveBeenCalledWith('[Notification] 🎯 Bounty Alert: 13 New Opportunities found');
    });

    test('should send notification for single opportunity', async () => {
      const result = await service.sendBountyAlert(1, []);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should limit opportunities to 10 in notification', async () => {
      const opportunities = Array.from({ length: 15 }, (_, i) => ({
        title: `Bounty ${i + 1}`,
        reward: 100 * (i + 1)
      }));

      const result = await service.sendBountyAlert(15, opportunities);

      expect(result.success).toBe(true);
      expect(result.notification.opportunities.length).toBe(10);
    });

    test('should handle invalid opportunity count', async () => {
      const result = await service.sendBountyAlert(-1, []);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid opportunity count');
    });

    test('should handle invalid opportunities array', async () => {
      const result = await service.sendBountyAlert(5, 'not an array');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Opportunities must be an array');
    });
  });

  describe('formatOpportunityDetails', () => {
    test('should format opportunity with all details', () => {
      const opportunity = {
        title: 'XSS Vulnerability',
        reward: 500,
        platform: 'HackerOne'
      };

      const formatted = service.formatOpportunityDetails(opportunity);
      expect(formatted).toBe('XSS Vulnerability - $500 (HackerOne)');
    });

    test('should handle missing reward', () => {
      const opportunity = {
        title: 'SQL Injection',
        platform: 'Bugcrowd'
      };

      const formatted = service.formatOpportunityDetails(opportunity);
      expect(formatted).toBe('SQL Injection - Reward not specified (Bugcrowd)');
    });

    test('should handle missing title', () => {
      const opportunity = {
        reward: 1000,
        platform: 'YesWeHack'
      };

      const formatted = service.formatOpportunityDetails(opportunity);
      expect(formatted).toBe('Untitled - $1000 (YesWeHack)');
    });

    test('should handle invalid opportunity', () => {
      expect(service.formatOpportunityDetails(null)).toBe('Invalid opportunity');
      expect(service.formatOpportunityDetails(undefined)).toBe('Invalid opportunity');
      expect(service.formatOpportunityDetails('string')).toBe('Invalid opportunity');
    });
  });
});
