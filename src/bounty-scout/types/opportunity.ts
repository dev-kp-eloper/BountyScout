export interface BountyOpportunity {
  id: string;
  title: string;
  url: string | null;
  repository: string | null;
  comments: number;
  lastUpdated: string;
  bountyAmount: number | null;
  type: string;
  status: 'active' | 'discarded' | 'pending';
  notes?: string | null;
}

export interface GitHubIssue {
  id: string;
  title: string;
  url: string;
  repository: string;
  comments: number;
  lastUpdated: string;
}