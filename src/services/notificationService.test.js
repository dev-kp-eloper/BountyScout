const { sendBountyAlert } = require('./notificationService');

describe('sendBountyAlert', () => {
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  test('sends notification for valid opportunity count', async () => {
    const result = await sendBountyAlert(19);
    
    expect(result.success).toBe(true);
    expect(result.message).toBe('🎯 Bounty Alert: 19 New Opportunities found');
    expect(result.count).toBe(19);
    expect(result.timestamp).toBeDefined();
    expect(consoleLogSpy).toHaveBeenCalled();
  });

  test('sends notification for single opportunity', async () => {
    const result = await sendBountyAlert(1);
    
    expect(result.success).toBe(true);
    expect(result.message).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('handles zero opportunities', async () => {
    const result = await sendBountyAlert(0);
    
    expect(result.success).toBe(true);
    expect(result.count).toBe(0);
  });

  test('handles invalid opportunity count', async () => {
    const result = await sendBountyAlert(-1);
    
    expect(result.success).toBe(false);
    expect(result.error).toBe('Invalid opportunity count');
    expect(consoleErrorSpy).toHaveBeenCalled();
  });

  test('includes additional options in result', async () => {
    const options = { channel: 'slack', priority: 'high' };
    const result = await sendBountyAlert(19, options);
    
    expect(result.success).toBe(true);
    expect(result.channel).toBe('slack');
    expect(result.priority).toBe('high');
  });
});
