import { deduplicateOpportunities, groupByRepository } from '../../../src/bounty-scout/utils/array';
import { BountyOpportunity } from '../../../src/bounty-scout/types/opportunity';

describe('array utils', () => {
  describe('deduplicateOpportunities', () => {
    it('should remove duplicates based on repository and id', () => {
      const opportunities: BountyOpportunity[] = [
        {
          id: '1',
          title: 'Test',
          url: 'https://example.com/1',
          repository: 'test/repo',
          comments: 0,
          lastUpdated: '2026-09-25T00:00:00Z',
          bountyAmount: null,
          type: 'Test',
          status: 'active'
        },
        {
          id: '1',
          title: 'Duplicate',
          url: 'https://example.com/2',
          repository: 'test/repo',
          comments: 1,
          lastUpdated: '2026-09-25T00:00:01Z',
          bountyAmount: null,
          type: 'Test',
          status: 'active'
        }
      ];
      
      const result = deduplicateOpportunities(opportunities);
      expect(result).toHaveLength(1);
    });
  });

  describe('groupByRepository', () => {
    it('should group opportunities by repository', () => {
      const opportunities: BountyOpportunity[] = [
        {
          id: '1',
          title: 'Test 1',
          url: 'https://example.com/1',
          repository: 'repo1',
          comments: 0,
          lastUpdated: '2026-09-25T00:00:00Z',
          bountyAmount: null,
          type: 'Test',
          status: 'active'
        },
        {
          id: '2',
          title: 'Test 2',
          url: 'https://example.com/2',
          repository: 'repo2',
          comments: 1,
          lastUpdated: '2026-09-25T00:00:01Z',
          bountyAmount: null,
          type: 'Test',
          status: 'active'
        }
      ];
      
      const result = groupByRepository(opportunities);
      expect(Object.keys(result)).toHaveLength(2);
      expect(result['repo1']).toHaveLength(1);
      expect(result['repo2']).toHaveLength(1);
    });
  });
});