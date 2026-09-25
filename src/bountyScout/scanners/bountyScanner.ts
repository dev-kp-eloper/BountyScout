import { BountyAlert, BountyScanner } from '../types';
import { fetchGitHubIssue } from '../utils/github';
import { parseBountyProposal } from '../utils/parser';

export class BasedHardwareBountyScanner implements BountyScanner {
  private readonly repo = 'BasedHardware/omi';
  private readonly issueNumber = 18738;

  async scan(): Promise<BountyAlert | null> {
    try {
      const issue = await fetchGitHubIssue(this.repo, this.issueNumber);
      if (!issue) return null;

      const bounty = parseBountyProposal(issue);
      if (!bounty) return null;

      return {
        repo: this.repo,
        issueNumber: this.issueNumber,
        title: bounty.title,
        description: bounty.description,
        amount: bounty.amount,
        url: issue.html_url,
        lastUpdated: issue.updated_at,
        severity: 'medium',
        tags: ['security', 'voip', 'exception-leak']
      };
    } catch (error) {
      console.error(`Failed to scan bounty for ${this.repo}#${this.issueNumber}:`, error);
      return null;
    }
  }
}
