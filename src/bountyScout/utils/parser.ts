import { GitHubIssue } from '../types';

export interface BountyProposal {
  title: string;
  description: string;
  amount: number;
}

export function parseBountyProposal(issue: GitHubIssue): BountyProposal | null {
  if (!issue.title.includes('($')) return null;

  const amountMatch = issue.title.match(/\$(\d+)/);
  if (!amountMatch) return null;

  const amount = parseInt(amountMatch[1], 10);
  const titleParts = issue.title.split('($')[0].trim();
  const description = issue.body?.replace(/\s+/g, ' ').trim() || '';

  return {
    title: titleParts,
    description,
    amount
  };
}
