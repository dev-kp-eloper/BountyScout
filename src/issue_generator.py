"""Utilities for generating GitHub issue bodies for bounty alerts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

# Template for the issue title.  The placeholder `{count}` will be replaced
# with the number of new opportunities found.  The original implementation
# contained a typo ("Opportunityies") which broke the expected wording
# and caused downstream tests to fail.  This has been corrected to
# "Opportunities".
ISSUE_TITLE_TEMPLATE = "🎯 Bounty Alert: {count} New Opportunities found"

# Template for the issue body header.
ISSUE_BODY_HEADER = (
    "### Active Bounty Scan Results\n\n"
    "**Scan Time:** {scan_time} UTC\n\n"
    "#### {index}. [{title}]({url})\n"
    "- **Repository:** [{repo_name}]({repo_url})\n"
    "- **Comments:** {comments}\n"
    "- **Last Updated:** {updated_at}\n"
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def format_scan_time(dt: datetime) -> str:
    """Return a formatted UTC timestamp string for the scan time."""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def build_issue_title(new_opportunity_count: int) -> str:
    """
    Build the GitHub issue title for a bounty alert.

    Parameters
    ----------
    new_opportunity_count: int
        Number of new bounty opportunities discovered in the latest scan.

    Returns
    -------
    str
        The formatted issue title.
    """
    # Use the corrected template (typo fixed)
    return ISSUE_TITLE_TEMPLATE.format(count=new_opportunity_count)


def build_issue_body(scan_results: List[Dict]) -> str:
    """
    Build the markdown body for the bounty alert issue.

    Parameters
    ----------
    scan_results: List[Dict]
        A list of dictionaries, each representing a single bounty scan result.
        Expected keys: title, url, repo_name, repo_url, comments, updated_at.

    Returns
    -------
    str
        The complete markdown body for the issue.
    """
    now = datetime.now(timezone.utc)
    lines: List[str] = [
        "### Active Bounty Scan Results",
        "",
        f"**Scan Time:** {format_scan_time(now)}",
        "",
    ]

    for idx, result in enumerate(scan_results, start=1):
        # Defensive programming: ensure all required keys exist.
        title = result.get("title", "Untitled")
        url = result.get("url", "#")
        repo_name = result.get("repo_name", "unknown/unknown")
        repo_url = result.get("repo_url", "#")
        comments = result.get("comments", 0)
        updated_at = result.get("updated_at", "unknown")

        lines.extend(
            [
                f"#### {idx}. [{title}]({url})",
                f"- **Repository:** [{repo_name}]({repo_url})",
                f"- **Comments:** {comments}",
                f"- **Last Updated:** {updated_at}",
                "",
            ]
        )

    # Join with newlines – GitHub renders markdown correctly.
    return "\n".join(lines).strip()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def generate_bounty_alert_issue(scan_results: List[Dict]) -> Dict[str, str]:
    """
    Generate a dictionary containing the title and body for a bounty alert
    GitHub issue.

    Parameters
    ----------
    scan_results: List[Dict]
        The raw scan results to be rendered.

    Returns
    -------
    Dict[str, str]
        Mapping with keys ``title`` and ``body`` ready for GitHub API consumption.
    """
    title = build_issue_title(len(scan_results))
    body = build_issue_body(scan_results)
    return {"title": title, "body": body}
