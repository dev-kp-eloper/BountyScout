export interface GitHubIssue {
  title: string;
  body: string | null;
  html_url: string;
  updated_at: string;
}

export interface BountyAlert {
  repo: string;
  issueNumber: number;
  title: string;
  description: string;
  amount: number;
  url: string;
  lastUpdated: string;
  severity: 'low' | 'medium' | 'high';
  tags: string[];
}

export interface BountyScanner {
  scan(): Promise<BountyAlert | null>;
}
