import { BountyOpportunity } from '../types/opportunity';
import { GitHubIssue } from '../types/github';
import { deduplicateOpportunities } from '../utils/array';

export class BountyScanner {
  private static readonly VALID_REPOSITORIES = [
    'CitrateNetwork/citrate-chain',
    'BasedHardware/omi',
    'Smartdevs17/stellarlend',
    'zhangjiayang6835-cyber/bounty-plaza'
  ];

  public static async scanIssues(issues: GitHubIssue[]): Promise<BountyOpportunity[]> {
    const validIssues = issues.filter(issue => {
      const repoMatch = this.VALID_REPOSITORIES.includes(issue.repository);
      const hasTitle = issue.title.trim().length > 0;
      return repoMatch && hasTitle;
    });

    return deduplicateOpportunities(validIssues.map(issue => {
      const [id, ...rest] = issue.title.split(':');
      const bountyAmount = this.extractBountyAmount(issue.title);
      
      return {
        id: id.trim() || issue.id,
        title: rest.join(':').trim(),
        url: issue.url,
        repository: issue.repository,
        comments: issue.comments,
        lastUpdated: issue.lastUpdated,
        bountyAmount,
        type: this.determineIssueType(issue.title),
        status: 'active',
        notes: this.extractNotes(issue.title)
      };
    }));
  }

  private static extractBountyAmount(title: string): number | null {
    const match = title.match(/\$(\d+) proposed/);
    return match ? parseInt(match[1]) : null;
  }

  private static determineIssueType(title: string): string {
    if (title.includes('[Bounty proposal]') || title.includes('[Bounty]')) {
      return 'Bounty proposal';
    }
    if (title.includes('[BUG BOUNTY]')) {
      return 'BUG BOUNTY';
    }
    if (title.includes('PBA-L2-')) {
      return 'PBA-L2 Issue';
    }
    if (title.includes('INFO residuals') || title.includes('residual:')) {
      return 'Audit residual';
    }
    if (title.includes('deferred:')) {
      return 'Deferred feature';
    }
    return 'General issue';
  }

  private static extractNotes(title: string): string | null {
    const deferredMatch = title.match(/deferred:\s*(.*)/);
    if (deferredMatch) return deferredMatch[1].trim();
    return null;
  }
}