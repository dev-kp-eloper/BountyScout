const { sendBountyNotification } = require('../src/services/notificationService');

describe('sendBountyNotification', () => {
  let consoleSpy;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation();
  });

  afterEach(() => {
    consoleSpy.mockRestore();
  });

  test('should send notification successfully', async () => {
    const result = await sendBountyNotification(19);
    
    expect(result.success).toBe(true);
    expect(result.message).toBe('🎯 Bounty Alert: 19 New Opportunities found');
    expect(consoleSpy).toHaveBeenCalledWith('🎯 Bounty Alert: 19 New Opportunities found');
  });

  test('should send notification through channels', async () => {
    const mockChannel = {
      send: jest.fn().mockResolvedValue(true)
    };

    const result = await sendBountyNotification(5, {
      channels: [mockChannel]
    });

    expect(result.success).toBe(true);
    expect(mockChannel.send).toHaveBeenCalledWith('🎯 Bounty Alert: 5 New Opportunities found');
  });

  test('should handle errors gracefully', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    
    const result = await sendBountyNotification('invalid');
    
    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
    
    consoleErrorSpy.mockRestore();
  });
});
