export interface BountyOpportunity {
  title: string;
  url: string;
  repository: string;
  comments: number;
  lastUpdated: string;
}

export class ReportGenerator {
  /**
   * Gera um relatório formatado em Markdown para as oportunidades encontradas.
   * @param opportunities Lista de oportunidades de bounty.
   * @param scanTime Timestamp da execução do scan.
   */
  public static generateMarkdownReport(opportunities: BountyOpportunity[], scanTime: string): string {
    let report = `### Active Bounty Scan Results\n\n`;
    report += `**Scan Time:** ${scanTime}\n\n`;

    if (opportunities.length === 0) {
      report += `*No new opportunities found during this scan.*\n`;
      return report;
    }

    opportunities.forEach((op, index) => {
      report += `#### ${index + 1}. [${op.title}](${op.url})\n`;
      report += `- **Repository:** [${op.repository}](${op.url.replace('/issues/', '/')})\n`;
      report += `- **Comments:** ${op.comments}\n`;
      report += `- **Last Updated:** ${op.lastUpdated}\n\n`;
    });

    return report;
  }
}
