import pytest
from datetime import datetime, timezone

from bounty_scout.issue_generator import build_issue_title, build_issue_body

def test_build_issue_title():
    # The title should correctly pluralize and contain the proper spelling.
    assert build_issue_title(5) == "🎯 Bounty Alert: 5 New Opportunities found"

def test_build_issue_body():
    # Prepare a deterministic scan result list.
    scan_results = [
        {
            "title": "Sample Bounty",
            "url": "https://github.com/example/repo/issues/1",
            "repo_name": "example/repo",
            "repo_url": "https://github.com/example/repo",
            "comments": 2,
            "updated_at": "2026-10-12T17:31:00Z",
        }
    ]

    body = build_issue_body(scan_results)

    # Verify that the body contains the expected sections and formatting.
    assert "### Active Bounty Scan Results" in body
    assert "**Scan Time:**" in body
    assert "#### 1. [Sample Bounty" in body
    assert "- **Repository**:" in body
    assert "- **Comments**:" in body
    assert "- **Last Updated**:" in body
