"""Unit tests for the BountyScout utility functions, triage filter, and notification formats."""

import os
import json
import tempfile
import unittest

from scout_bounties import (
    is_clean_candidate,
    format_issue_title,
    format_issue_body,
    format_notification_message,
    load_seen_bounties,
    save_seen_bounties,
    MAX_COMMENTS,
)


class TestBountyScout(unittest.TestCase):
    """Test suite covering triage logic, formatting, and persistence."""

    def setUp(self):
        """Set up standard test fixture objects."""
        self.valid_item = {
            "title": "Implement feature X for bounty reward",
            "body": "We offer $100 for implementing this feature.",
            "state": "open",
            "comments": 2,
            "html_url": "https://github.com/org/repo/issues/10",
            "assignees": [],
        }

    def test_is_clean_candidate_valid(self):
        """Verify that a standard open unassigned issue qualifies as a clean candidate."""
        self.assertTrue(is_clean_candidate(self.valid_item))

    def test_is_clean_candidate_filters_pull_requests(self):
        """Verify that pull request objects returned in search results are filtered out."""
        pr_item = dict(self.valid_item, pull_request={"url": "https://api.github.com/..."})
        self.assertFalse(is_clean_candidate(pr_item))

    def test_is_clean_candidate_filters_closed_or_locked(self):
        """Verify that closed or locked issues are excluded from results."""
        closed_item = dict(self.valid_item, state="closed")
        self.assertFalse(is_clean_candidate(closed_item))
        locked_item = dict(self.valid_item, state="open", locked=True)
        self.assertFalse(is_clean_candidate(locked_item))

    def test_is_clean_candidate_filters_assignees(self):
        """Verify that issues with active assignees are excluded."""
        assigned_item = dict(self.valid_item, assignees=[{"login": "developer"}])
        self.assertFalse(is_clean_candidate(assigned_item))
        assigned_single = dict(self.valid_item, assignee={"login": "developer"}, assignees=[])
        self.assertFalse(is_clean_candidate(assigned_single))

    def test_is_clean_candidate_filters_overcrowded_threads(self):
        """Verify that issues exceeding the maximum comment limit are rejected."""
        overcrowded_item = dict(self.valid_item, comments=MAX_COMMENTS + 1)
        self.assertFalse(is_clean_candidate(overcrowded_item))

    def test_is_clean_candidate_filters_recursive_alerts(self):
        """Verify that automated alert issues and BountyScout repository issues are rejected."""
        alert_item_1 = dict(self.valid_item, title="🎯 Bounty Alert: 2 New Opportunities found")
        self.assertFalse(is_clean_candidate(alert_item_1))

        alert_item_2 = dict(self.valid_item, title="Daily Bounty Alert digest")
        self.assertFalse(is_clean_candidate(alert_item_2))

        fork_item = dict(self.valid_item, html_url="https://github.com/someone/BountyScout/issues/5")
        self.assertFalse(is_clean_candidate(fork_item))

        self_repo_item = dict(self.valid_item, html_url="https://github.com/my-org/my-repo/issues/12")
        self.assertFalse(is_clean_candidate(self_repo_item, current_repo="my-org/my-repo"))

    def test_is_clean_candidate_filters_spam_and_crypto(self):
        """Verify that all spam keywords trigger rejection."""
        spam_cases = [
            {"title": "Join our crypto airdrop now", "body": "Free tokens"},
            {"title": "Need referral promotion", "body": "Bounty reward"},
            {"title": "Build casino gambling game", "body": "Good pay"},
            {"title": "Automated trading bot script", "body": "Crypto bot"},
            {"title": "Write blog post about project", "body": "Article writing required"},
            {"title": "Tutorial proposal submission", "body": "Need content creator"},
            {"title": "Claim testnet faucet tokens", "body": "Faucet distribution"},
            {"title": "Mega community giveaway", "body": "Join discord"},
        ]
        for case in spam_cases:
            spam_item = dict(self.valid_item, title=case["title"], body=case["body"])
            self.assertFalse(is_clean_candidate(spam_item), f"Failed to filter spam: {case['title']}")

    def test_is_clean_candidate_handles_non_dict_and_none_fields(self):
        """Verify that non-dictionary objects or missing/None fields do not raise exceptions."""
        self.assertFalse(is_clean_candidate(None))
        self.assertFalse(is_clean_candidate("not a dict"))
        none_fields_item = {
            "title": None,
            "body": None,
            "state": "open",
            "comments": None,
            "assignees": None,
            "html_url": None,
        }
        self.assertTrue(is_clean_candidate(none_fields_item))

    def test_format_issue_title_singular(self):
        """Verify proper singular grammar for single opportunity."""
        title = format_issue_title(1)
        self.assertEqual(title, "🎯 Bounty Alert: 1 New Opportunity found")

    def test_format_issue_title_plural(self):
        """Verify proper plural grammar without spelling typos for multiple opportunities."""
        title = format_issue_title(2)
        self.assertEqual(title, "🎯 Bounty Alert: 2 New Opportunities found")
        self.assertNotIn("Opportunityies", title)

        title_large = format_issue_title(15)
        self.assertEqual(title_large, "🎯 Bounty Alert: 15 New Opportunities found")

    def test_format_notification_message_singular_and_plural(self):
        """Verify notification message formatting for singular and plural counts."""
        single_bounty = [{
            "title": "Bug Fix",
            "repo": "owner/repo",
            "comments": 1,
            "url": "https://github.com/owner/repo/issues/1",
        }]
        msg_single = format_notification_message(single_bounty, now_str="2026-08-29 12:00 UTC")
        self.assertIn("Found 1 new opportunity:", msg_single)

        multiple_bounties = [
            {
                "title": "Bug Fix 1",
                "repo": "owner/repo",
                "comments": 1,
                "url": "https://github.com/owner/repo/issues/1",
            },
            {
                "title": "Feature 2",
                "repo": "owner/repo2",
                "comments": 3,
                "url": "https://github.com/owner/repo2/issues/2",
            }
        ]
        msg_plural = format_notification_message(multiple_bounties, now_str="2026-08-29 12:00 UTC")
        self.assertIn("Found 2 new opportunities:", msg_plural)
        self.assertNotIn("opportunityies", msg_plural)

    def test_format_issue_body(self):
        """Verify markdown structure of the generated issue body."""
        bounties = [{
            "title": "Add feature",
            "url": "https://github.com/test/repo/issues/42",
            "repo": "test/repo",
            "comments": 0,
            "updated_at": "2026-08-29T10:00:00Z"
        }]
        body = format_issue_body(bounties, now_str="2026-08-29 12:00 UTC")
        self.assertIn("### Active Bounty Scan Results", body)
        self.assertIn("**Scan Time:** 2026-08-29 12:00 UTC", body)
        self.assertIn("#### 1. [Add feature](https://github.com/test/repo/issues/42)", body)
        self.assertIn("- **Repository:** [test/repo](https://github.com/test/repo)", body)
        self.assertIn("- **Comments:** 0", body)

    def test_load_and_save_seen_bounties(self):
        """Verify reading, writing, and error recovery for seen bounty state JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_state_file = os.path.join(tmpdir, "test_seen.json")

            loaded = load_seen_bounties(temp_state_file)
            self.assertEqual(loaded, set())

            test_urls = {"https://github.com/a/b/issues/1", "https://github.com/c/d/issues/2"}
            save_seen_bounties(test_urls, temp_state_file)

            reloaded = load_seen_bounties(temp_state_file)
            self.assertEqual(reloaded, test_urls)

            with open(temp_state_file, "w", encoding="utf-8") as f:
                f.write("{invalid json]")
            self.assertEqual(load_seen_bounties(temp_state_file), set())


if __name__ == "__main__":
    unittest.main()
