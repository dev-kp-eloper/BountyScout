import { BountyOpportunity } from '../types/opportunity';

export function deduplicateOpportunities(
  opportunities: BountyOpportunity[]
): BountyOpportunity[] {
  const seen = new Map<string, boolean>();
  return opportunities.filter(opportunity => {
    const key = `${opportunity.repository}|${opportunity.id}`;
    if (seen.has(key)) {
      return false;
    }
    seen.set(key, true);
    return true;
  });
}

export function groupByRepository(
  opportunities: BountyOpportunity[]
): Record<string, BountyOpportunity[]> {
  return opportunities.reduce((acc, opportunity) => {
    if (!acc[opportunity.repository]) {
      acc[opportunity.repository] = [];
    }
    acc[opportunity.repository].push(opportunity);
    return acc;
  }, {} as Record<string, BountyOpportunity[]>);
}