const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
    jest.spyOn(console, 'log').mockImplementation();
    jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('sendBountyAlert', () => {
    test('should send alert with correct message for 13 opportunities', async () => {
      const result = await service.sendBountyAlert(13, []);
      
      expect(result.success).toBe(true);
      expect(result.message).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.count).toBe(13);
      expect(result.timestamp).toBeDefined();
      expect(console.log).toHaveBeenCalledWith('🎯 Bounty Alert: 13 New Opportunities found');
    });

    test('should send alert with correct message for 1 opportunity', async () => {
      const result = await service.sendBountyAlert(1, []);
      
      expect(result.success).toBe(true);
      expect(result.message).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should handle zero opportunities', async () => {
      const result = await service.sendBountyAlert(0, []);
      
      expect(result.success).toBe(true);
      expect(result.message).toBe('🎯 Bounty Alert: No new opportunities found');
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
    test('should format multiple opportunities correctly', () => {
      const opportunities = [
        { title: 'Bug Fix', reward: '$500', url: 'https://example.com/1' },
        { title: 'Feature Request', reward: '$1000', url: 'https://example.com/2' }
      ];
      
      const result = service.formatOpportunityDetails(opportunities);
      
      expect(result).toContain('1. Bug Fix - Reward: $500');
      expect(result).toContain('2. Feature Request - Reward: $1000');
    });

    test('should handle empty array', () => {
      const result = service.formatOpportunityDetails([]);
      expect(result).toBe('No opportunities to display');
    });

    test('should handle opportunities with missing fields', () => {
      const opportunities = [
        { title: 'Test' }
      ];
      
      const result = service.formatOpportunityDetails(opportunities);
      expect(result).toContain('Test - Reward: N/A');
    });
  });
});
