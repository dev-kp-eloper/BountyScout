const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
  });

  test('should subscribe and receive notifications', () => {
    const mockCallback = jest.fn();
    service.subscribe(mockCallback);

    const opportunities = [
      { id: 1, title: 'Bug Fix', reward: 100 },
      { id: 2, title: 'Feature Request', reward: 200 }
    ];

    service.sendBountyAlert(2, opportunities);

    expect(mockCallback).toHaveBeenCalledTimes(1);
    expect(mockCallback).toHaveBeenCalledWith(
      expect.objectContaining({
        message: '🎯 Bounty Alert: 2 New Opportunities found',
        count: 2,
        opportunities
      })
    );
  });

  test('should handle multiple subscribers', () => {
    const mockCallback1 = jest.fn();
    const mockCallback2 = jest.fn();
    
    service.subscribe(mockCallback1);
    service.subscribe(mockCallback2);

    service.sendBountyAlert(13);

    expect(mockCallback1).toHaveBeenCalledTimes(1);
    expect(mockCallback2).toHaveBeenCalledTimes(1);
  });

  test('should unsubscribe correctly', () => {
    const mockCallback = jest.fn();
    service.subscribe(mockCallback);
    service.unsubscribe(mockCallback);

    service.sendBountyAlert(1);

    expect(mockCallback).not.toHaveBeenCalled();
  });

  test('should handle subscriber errors gracefully', () => {
    const errorCallback = jest.fn(() => {
      throw new Error('Subscriber error');
    });
    const goodCallback = jest.fn();

    service.subscribe(errorCallback);
    service.subscribe(goodCallback);

    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

    service.sendBountyAlert(5);

    expect(errorCallback).toHaveBeenCalled();
    expect(goodCallback).toHaveBeenCalled();
    expect(consoleSpy).toHaveBeenCalled();

    consoleSpy.mockRestore();
  });

  test('should throw error for invalid subscriber', () => {
    expect(() => service.subscribe('not a function')).toThrow('Callback must be a function');
  });

  test('should include timestamp in notification', () => {
    const mockCallback = jest.fn();
    service.subscribe(mockCallback);

    service.sendBountyAlert(1);

    expect(mockCallback).toHaveBeenCalledWith(
      expect.objectContaining({
        timestamp: expect.any(String)
      })
    );
  });
});
