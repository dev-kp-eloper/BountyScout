import { BountyOpportunity } from '../types/bounty';

export class BountyAlertParser {
  /**
   * Parses the raw text from a Bounty Alert scan result.
   * Format: 
   * #### [Title](Link)
   * - **Repository:** [RepoName](RepoLink)
   * - **Comments:** X
   * - **Last Updated:** Timestamp
   */
  public static parse(rawText: string): BountyOpportunity[] {
    const opportunities: BountyOpportunity[] = [];
    const sections = rawText.split('#### ');

    // Skip the first section (Scan Time header)
    for (let i = 1; i < sections.length; i++) {
      const section = sections[i];
      
      try {
        const titleLineMatch = section.match(/^\[(.*?)\]\((.*?)\)/);
        const repoLineMatch = section.match(/- \*\*Repository:\*\* \[(.*?)\]\((.*?)\)/);
        const commentsLineMatch = section.match(/- \*\*Comments:\*\* (\d+)/);
        const updatedLineMatch = section.match(/- \*\*Last Updated:\*\* (.*)/);

        if (titleLineMatch && repoLineMatch) {
          const fullTitle = titleLineMatch[1];
          const issueUrl = titleLineMatch[2];
          const repoName = repoLineMatch[1];
          const repoUrl = repoLineMatch[2];
          const comments = commentsLineMatch ? parseInt(commentsLineMatch[1], 10) : 0;
          const lastUpdated = updatedLineMatch ? updatedLineMatch[1].trim() : new Date().toISOString();

          // Extract bounty amount if present in title (e.g., "$60")
          const amountMatch = fullTitle.match(/\$(\d+)/);
          const amount = amountMatch ? parseInt(amountMatch[1], 10) : 0;

          opportunities.push({
            title: fullTitle,
            url: issueUrl,
            repository: repoName,
            repositoryUrl: repoUrl,
            amount: amount,
            comments,
            lastUpdated: new Date(lastUpdated),
            status: 'new'
          });
        }
      } catch (error) {
        console.error(`Failed to parse section ${i}:`, error);
        continue;
      }
    }

    return opportunities;
  }
}
