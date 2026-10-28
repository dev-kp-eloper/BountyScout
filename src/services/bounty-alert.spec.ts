import { BountyAlertService } from './bounty-alert.service';
import { BountyOpportunity } from '../types/bounty.types';

describe('BountyAlertService', () => {
  let service: BountyAlertService;

  beforeEach(() => {
    service = new BountyAlertService();
  });

  it('should format bounty opportunities correctly', () => {
    const mockOpportunities: BountyOpportunity[] = [
      {
        id: 1,
        title: 'Test Vulnerability',
        url: 'https://github.com/test/repo/issues/1',
        repository: 'test/repo',
        repoUrl: 'https://github.com/test/repo',
        comments: 0,
        lastUpdated: '2026-10-25T13:00:18Z'
      }
    ];

    const result = service.formatBountyAlert(mockOpportunities);
    expect(result).toContain('1 New Opportunities found');
    expect(result).toContain('Test Vulnerability');
  });
});
