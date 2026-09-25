import { BountyScanner } from '../../../src/bounty-scout/services/scanner';
import { GitHubIssue } from '../../../src/bounty-scout/types/opportunity';

describe('BountyScanner', () => {
  describe('scanIssues', () => => {
    it('should filter invalid repositories', async () => {
      const issues: GitHubIssue[] = [
        {
          id: '1',
          title: 'Test issue',
          url: 'https://github.com/invalid/repo/issues/1',
          repository: 'invalid/repo',
          comments: 0,
          lastUpdated: '2026-09-25T00:00:00Z'
        }
      ];
      
      const result = await BountyScanner.scanIssues(issues);
      expect(result).toHaveLength(0);
    });

    it('should extract bounty amount when present', async () => {
      const issues: GitHubIssue[] = [
        {
          id: '18852',
          title: '[Bounty proposal] fix: test ($50 proposed)',
          url: 'https://github.com/BasedHardware/omi/issues/18852',
          repository: 'BasedHardware/omi',
          comments: 1,
          lastUpdated: '2026-09-25T00:00:00Z'
        }
      ];
      
      const result = await BountyScanner.scanIssues(issues);
      expect(result[0].bountyAmount).toBe(50);
    });

    it('should handle PBA-L2 issue types correctly', async () => {
      const issues: GitHubIssue[] = [
        {
          id: '216',
          title: 'PBA-L2-011: test issue',
          url: 'https://github.com/CitrateNetwork/citrate-chain/issues/216',
          repository: 'CitrateNetwork/citrate-chain',
          comments: 0,
          lastUpdated: '2026-09-25T00:00:00Z'
        }
      ];
      
      const result = await BountyScanner.scanIssues(issues);
      expect(result[0].type).toBe('PBA-L2 Issue');
      expect(result[0].id).toBe('PBA-L2-011');
    });

    it('should handle deferred issues with notes', async () => {
      const issues: GitHubIssue[] = [
        {
          id: '213',
          title: 'PBA-L2-048: test issue (deferred: UUPS upgrade ceremony)',
          url: 'https://github.com/CitrateNetwork/citrate-chain/issues/213',
          repository: 'CitrateNetwork/citrate-chain',
          comments: 0,
          lastUpdated: '2026-09-25T00:00:00Z'
        }
      ];
      
      const result = await BountyScanner.scanIssues(issues);
      expect(result[0].notes).toBe('UUPS upgrade ceremony');
    });
  });
});