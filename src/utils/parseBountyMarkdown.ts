```ts
/**
 * Utility to parse the markdown output of the BountyScout scan.
 *
 * The scan output is a markdown string that contains a list of bounties in the
 * following format:
 *
 *   1. [[Bounty: $60] Pin the documented 422 for unsupported assets in the persist e2e](https://github.com/Nudge-Pay/nudge-server/issues/11)
 *   - **Repository:** [Nudge-Pay/nudge-server](https://github.com/Nudge-Pay/nudge-server)
 *   - **Comments:** 2
 *   - **Last Updated:** 2026-10-10T13:19:25Z
 *
 * This parser extracts the relevant fields into a typed array of `Bounty`
 * objects. It is tolerant to minor formatting variations and ignores
 * lines that do not match the expected pattern.
 */

export interface Bounty {
  /** The issue number extracted from the title, if available. */
  id: number | null;
  /** The full title of the bounty (including any tags). */
  title: string;
  /** The URL to the GitHub issue. */
  url: string;
  /** The repository name (owner/repo). */
  repository: string;
  /** Number of comments on the issue. */
  comments: number;
  /** ISO timestamp of the last update. */
  lastUpdated: string;
}

/**
 * Parses a markdown string produced by the BountyScout scan into an array of
 * {@link Bounty} objects.
 *
 * @param markdown The raw markdown string from the scan.
 * @returns An array of parsed bounties.
 */
export function parseBountyMarkdown(markdown: string): Bounty[] {
  const lines = markdown.split('\n');
  const bounties: Bounty[] = [];

  // Regex to capture the main list item line.
  // Example: 1. [[Bounty: $60] Pin the documented 422 for unsupported assets in the persist e2e](https://github.com/Nudge-Pay/nudge-server/issues/11)
  const itemRegex = /^\s*\d+\.\s*\[([^\]]+)\]\(([^)]+)\)/;

  // Regex to capture the repository line.
  // Example: - **Repository:** [Nudge-Pay/nudge-server](https://github.com/Nudge-Pay/nudge-server)
  const repoRegex = /^\s*-\s*\*\*Repository:\*\*\s*\[([^\]]+)\]\(([^)]+)\)/;

  // Regex to capture the comments line.
  // Example: - **Comments:** 2
  const commentsRegex = /^\s*-\s*\*\*Comments:\*\*\s*(\d+)/;

  // Regex to capture the last updated line.
  // Example: - **Last Updated:** 2026-10-10T13:19:25Z
  const updatedRegex = /^\s*-\s*\*\*Last Updated:\*\*\s*([^\s]+)/;

  let current: Partial<Bounty> = {};

  for (
