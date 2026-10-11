/**
 * Scanner module - Scans repositories for bounty issues
 */

const { Octokit } = require("@octokit/rest");
const config = require("./config");
const logger = require("./logger");

async function scanRepositories(targets) {
  const octokit = new Octokit({
    auth: config.githubToken,
  });

  const allBounties = [];

  for (const target of targets) {
    logger.debug(`Scanning ${target.owner}/${target.repo}...`);
    
    try {
      const issues = await octokit.paginate(octokit.issues.listForRepo, {
        owner: target.owner,
        repo: target.repo,
        state: "all",
        per_page: 100,
        sort: "updated",
        direction: "desc",
      });

      for (const issue of issues) {
        if (isBountyIssue(issue)) {
          allBounties.push({
            ...issue,
            repository: `${target.owner}/${target.repo}`,
            bounty: extractBounty(issue),
          });
        }
      }
    } catch (error) {
      logger.error(`Failed to scan ${target.owner}/${target.repo}: ${error.message}`);
    }
  }

  return allBounties;
}

function isBountyIssue(issue) {
  const labelNames = (issue.labels || []).map((l) => l.name.toLowerCase());
  const bodyLower = (issue.body || "").toLowerCase();
  const titleLower = (issue.title || "").toLowerCase();

  const hasBountyLabel = labelNames.some(
    (name) =>
      name.includes("bounty") ||
      name.includes("paid") ||
      name.includes("sponsored")
  );

  const hasBountyInTitle = titleLower.includes("bounty") || /\$\d+/.test(titleLower);
  const hasBountyInBody =
    bodyLower.includes("bounty") ||
    bodyLower.includes("paid") ||
    /\$\d+/.test(bodyLower);

  return hasBountyLabel || (hasBountyInTitle && hasBountyInBody);
}

function extractBounty(issue) {
  const body = issue.body || "";
  const title = issue.title || "";
  const combined = body + " " + title;

  const matches = combined.match(/\$\s*(\d+)/gi);
  if (matches && matches.length > 0) {
    return Math.max(...matches.map((m) => parseInt(m.replace(/[$\s]/g, ""), 10)));
  }
  return null;
}

module.exports = { scan: scanRepositories, isBountyIssue, extractBounty };
