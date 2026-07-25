const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  describe('sendBountyAlert', () => {
    test('sends alert for multiple opportunities', async () => {
      const opportunities = [
        { title: 'Bug Fix', reward: '$500', platform: 'GitHub' },
        { title: 'Feature Request', reward: '$1000', platform: 'GitLab' }
      ];

      const result = await service.sendBountyAlert(2, opportunities);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 2 New Opportunities found');
      expect(result.notification.count).toBe(2);
      expect(result.notification.opportunities).toHaveLength(2);
    });

    test('sends alert for single opportunity', async () => {
      const opportunities = [{ title: 'Bug Fix', reward: '$500', platform: 'GitHub' }];

      const result = await service.sendBountyAlert(1, opportunities);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('limits opportunities in notification to 10', async () => {
      const opportunities = Array(15).fill({ title: 'Test', reward: '$100', platform: 'Test' });

      const result = await service.sendBountyAlert(15, opportunities);

      expect(result.success).toBe(true);
      expect(result.notification.opportunities).toHaveLength(10);
      expect(result.notification.hasMore).toBe(true);
    });

    test('handles zero opportunities', async () => {
      const result = await service.sendBountyAlert(0, []);

      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: No new opportunities found');
    });

    test('handles invalid count', async () => {
      const result = await service.sendBountyAlert(-1, []);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid opportunity count');
    });

    test('handles invalid opportunities array', async () => {
      const result = await service.sendBountyAlert(5, 'not an array');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Opportunities must be an array');
    });
  });

  describe('formatOpportunityDetails', () => {
    test('formats opportunity correctly', () => {
      const opportunity = {
        title: 'Fix typo in README',
        reward: '$100',
        platform: 'GitHub'
      };

      const formatted = service.formatOpportunityDetails(opportunity);
      expect(formatted).toBe('Fix typo in README - $100 (GitHub)');
    });

    test('handles missing fields', () => {
      const opportunity = {};
      const formatted = service.formatOpportunityDetails(opportunity);
      expect(formatted).toBe('Untitled - N/A (Unknown)');
    });

    test('handles invalid opportunity', () => {
      expect(service.formatOpportunityDetails(null)).toBe('Invalid opportunity');
      expect(service.formatOpportunityDetails('invalid')).toBe('Invalid opportunity');
    });
  });
});
