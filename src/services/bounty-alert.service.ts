import { BountyOpportunity } from '../types/bounty.types';

export class BountyAlertService {
  public formatBountyAlert(opportunities: BountyOpportunity[]): string {
    if (!opportunities || opportunities.length === 0) {
      return '🎯 No new bounty opportunities found.';
    }
    let alert = '🎯 Bounty Alert: ' + opportunities.length + ' New Opportunities found\n';
    opportunities.forEach((opp, index) => {
      alert += `${index + 1}. [${opp.title}](${opp.url})\n`;
      alert += `- **Repository:** [${opp.repository}](${opp.repoUrl})\n`;
      alert += `- **Comments:** ${opp.comments}\n`;
      alert += `- **Last Updated:** ${opp.lastUpdated}\n`;
    });
    return alert.trim();
  }
}
