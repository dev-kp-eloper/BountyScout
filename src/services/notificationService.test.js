const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
  });

  test('registers notification handlers', () => {
    const handler = jest.fn();
    service.registerHandler(handler);
    expect(service.notificationHandlers).toHaveLength(1);
  });

  test('throws error when registering non-function handler', () => {
    expect(() => service.registerHandler('not a function')).toThrow('Handler must be a function');
  });

  test('sends bounty alert with correct message', async () => {
    const handler = jest.fn();
    service.registerHandler(handler);

    await service.sendBountyAlert(13, []);

    expect(handler).toHaveBeenCalledWith(
      expect.objectContaining({
        message: '🎯 Bounty Alert: 13 New Opportunities found',
        count: 13,
        opportunities: [],
        timestamp: expect.any(String)
      })
    );
  });

  test('sends notifications to multiple handlers', async () => {
    const handler1 = jest.fn();
    const handler2 = jest.fn();
    service.registerHandler(handler1);
    service.registerHandler(handler2);

    await service.sendBountyAlert(5, []);

    expect(handler1).toHaveBeenCalled();
    expect(handler2).toHaveBeenCalled();
  });

  test('clears all handlers', () => {
    service.registerHandler(jest.fn());
    service.registerHandler(jest.fn());
    expect(service.notificationHandlers).toHaveLength(2);

    service.clearHandlers();
    expect(service.notificationHandlers).toHaveLength(0);
  });

  test('handles handler errors gracefully', async () => {
    const failingHandler = jest.fn(() => {
      throw new Error('Handler error');
    });
    const successHandler = jest.fn();
    
    service.registerHandler(failingHandler);
    service.registerHandler(successHandler);

    await service.sendBountyAlert(3, []);

    expect(failingHandler).toHaveBeenCalled();
    expect(successHandler).toHaveBeenCalled();
  });
});
