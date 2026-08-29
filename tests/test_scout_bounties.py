import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scout_bounties import (
    pluralize_opportunity,
    load_seen_bounties,
    save_seen_bounties,
    is_clean_candidate,
    format_notification_message,
    build_notification_markdown,
    format_github_issue_content,
    build_github_issue_payload,
)


class TestBountyScout(unittest.TestCase):
    def test_pluralize_opportunity(self):
        self.assertEqual(pluralize_opportunity(1, capitalize=False), "opportunity")
        self.assertEqual(pluralize_opportunity(1, capitalize=True), "Opportunity")
        self.assertEqual(pluralize_opportunity(0, capitalize=False), "opportunities")
        self.assertEqual(pluralize_opportunity(0, capitalize=True), "Opportunities")
        self.assertEqual(pluralize_opportunity(2, capitalize=False), "opportunities")
        self.assertEqual(pluralize_opportunity(2, capitalize=True), "Opportunities")
        self.assertEqual(pluralize_opportunity(15, capitalize=False), "opportunities")
        self.assertEqual(pluralize_opportunity(15, capitalize=True), "Opportunities")

    def test_is_clean_candidate_filters_pull_requests(self):
        pr_item = {
            "title": "Fix: Implement caching layer",
            "body": "This PR adds a redis cache",
            "html_url": "https://github.com/stellar/soroban-example/pull/12",
            "pull_request": {"url": "https://api.github.com/repos/stellar/soroban-example/pulls/12"},
            "assignees": [],
            "comments": 1,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(pr_item))

    def test_is_clean_candidate_filters_closed_and_locked(self):
        closed_item = {
            "title": "Add analytics SDK",
            "body": "Bounty for adding analytics",
            "html_url": "https://github.com/org/repo/issues/1",
            "assignees": [],
            "comments": 2,
            "state": "closed"
        }
        self.assertFalse(is_clean_candidate(closed_item))

        locked_item = {
            "title": "Add analytics SDK",
            "body": "Bounty for adding analytics",
            "html_url": "https://github.com/org/repo/issues/2",
            "assignees": [],
            "comments": 2,
            "state": "open",
            "locked": True
        }
        self.assertFalse(is_clean_candidate(locked_item))

    def test_is_clean_candidate_filters_assigned_issues(self):
        assigned_item_1 = {
            "title": "Build wallet connect modal",
            "body": "500 USDC bounty",
            "html_url": "https://github.com/org/repo/issues/3",
            "assignees": [{"login": "alice"}],
            "comments": 2,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(assigned_item_1))

        assigned_item_2 = {
            "title": "Build wallet connect modal",
            "body": "500 USDC bounty",
            "html_url": "https://github.com/org/repo/issues/4",
            "assignee": {"login": "bob"},
            "assignees": [],
            "comments": 1,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(assigned_item_2))

    def test_is_clean_candidate_filters_overcrowded_issues(self):
        crowded_item = {
            "title": "Implement multi-sig wallet support",
            "body": "Large bounty for multi-sig feature",
            "html_url": "https://github.com/org/repo/issues/5",
            "assignees": [],
            "comments": 26,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(crowded_item))

        borderline_item = {
            "title": "Design logo bounty",
            "body": "Offering bounty for logo",
            "html_url": "https://github.com/stellar-community/dex-core/issues/50",
            "assignees": [],
            "comments": 25,
            "state": "open"
        }
        self.assertTrue(is_clean_candidate(borderline_item))

    def test_is_clean_candidate_filters_recursive_bountyscout_and_alerts(self):
        # Case 1: External BountyScout repo alert
        bs_item_1 = {
            "title": "🎯 Bounty Alert: 6 New Opportunityies found",
            "body": "Active bounty scan results",
            "html_url": "https://github.com/freedom-winds/BountyScout/issues/898",
            "assignees": [],
            "comments": 0,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(bs_item_1))

        # Case 2: Another BountyScout fork
        bs_item_2 = {
            "title": "🎯 Bounty Alert: 2 New Opportunityies found",
            "body": "Active bounty scan results",
            "html_url": "https://github.com/vansh-09/BountyScout/issues/988",
            "assignees": [],
            "comments": 0,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(bs_item_2))

        # Case 3: Self repository match
        self_item = {
            "title": "Fix issue in scanner",
            "body": "Scanner bug description",
            "html_url": "https://github.com/vansh-09/BountyScout/issues/987",
            "assignees": [],
            "comments": 0,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(self_item, current_repo="vansh-09/BountyScout"))

        # Case 4: Alert title pattern without repo name
        alert_item = {
            "title": "🎯 Bounty Alert: 10 New Opportunities found",
            "body": "Scan results",
            "html_url": "https://github.com/another-org/random-repo/issues/12",
            "assignees": [],
            "comments": 0,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(alert_item))

        # Case 5: Label match
        labeled_item = {
            "title": "Some issue title",
            "body": "Some description",
            "html_url": "https://github.com/another-org/random-repo/issues/13",
            "labels": [{"name": "bounty-alert"}],
            "assignees": [],
            "comments": 0,
            "state": "open"
        }
        self.assertFalse(is_clean_candidate(labeled_item))

    def test_is_clean_candidate_filters_spam_blocklist(self):
        spam_samples = [
            ("Free token airdrop event", "Claim your free crypto tokens"),
            ("New referral reward program", "Sign up using referral link"),
            ("Online casino promotion", "Earn playing slots"),
            ("Automated trading bot bounty", "Build arbitrage trading bot"),
            ("Write a blog post for bounty", "Medium article writing needed"),
            ("Claim free crypto faucet tokens", "Daily faucet claims"),
            ("Giveaway retweet task", "Retweet to win prizes"),
            ("Telegram bot promo", "Join our channel")
        ]
        for title, body in spam_samples:
            item = {
                "title": title,
                "body": body,
                "html_url": "https://github.com/some-org/bounty-project/issues/1",
                "assignees": [],
                "comments": 0,
                "state": "open"
            }
            self.assertFalse(is_clean_candidate(item), f"Failed to filter spam: {title}")

    def test_is_clean_candidate_accepts_valid_bounty(self):
        valid_item = {
            "title": "🦀 [CONTRACT] Keeper Economic Bonding & On-Chain Stake Slashing Protocol",
            "body": "Implement economic bonding mechanism in Rust/Soroban",
            "html_url": "https://github.com/SoroLabs/SoroTask/issues/1043",
            "assignees": [],
            "comments": 4,
            "state": "open",
            "locked": False
        }
        self.assertTrue(is_clean_candidate(valid_item))

    def test_state_persistence(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_state_file = os.path.join(tmp_dir, "test_seen.json")
            
            # Initial load from non-existent file
            initial_seen = load_seen_bounties(temp_state_file)
            self.assertEqual(initial_seen, set())

            # Save URLs
            test_urls = {
                "https://github.com/org/repo1/issues/1",
                "https://github.com/org/repo2/issues/2"
            }
            save_seen_bounties(test_urls, temp_state_file)

            # Reload and verify
            reloaded_seen = load_seen_bounties(temp_state_file)
            self.assertEqual(reloaded_seen, test_urls)

            # Corrupt file handles gracefully
            with open(temp_state_file, "w") as f:
                f.write("{invalid_json:")
            corrupt_seen = load_seen_bounties(temp_state_file)
            self.assertEqual(corrupt_seen, set())

    def test_build_notification_markdown(self):
        now_str = "2026-08-29 12:00 UTC"
        
        # Single item
        single_item = [{
            "title": "Fix ZK-verifier bug",
            "repo": "zk-protocol/core",
            "comments": 1,
            "url": "https://github.com/zk-protocol/core/issues/100"
        }]
        msg_single = format_notification_message(single_item, now_str)
        self.assertIn("Found 1 new opportunity:", msg_single)
        self.assertNotIn("opportunityies", msg_single)
        self.assertIn("• Repository: `zk-protocol/core`", msg_single)
        self.assertIn("• Link: https://github.com/zk-protocol/core/issues/100", msg_single)

        # Reusable alias check
        alias_msg = build_notification_markdown(single_item, now_str)
        self.assertEqual(msg_single, alias_msg)

        # Multiple items
        multi_items = [
            {
                "title": "Fix issue 1",
                "repo": "org/repo1",
                "comments": 0,
                "url": "https://github.com/org/repo1/issues/1"
            },
            {
                "title": "Fix issue 2",
                "repo": "org/repo2",
                "comments": 2,
                "url": "https://github.com/org/repo2/issues/2"
            }
        ]
        msg_multi = format_notification_message(multi_items, now_str)
        self.assertIn("Found 2 new opportunities:", msg_multi)
        self.assertNotIn("opportunityies", msg_multi)

    def test_build_github_issue_payload(self):
        now_str = "2026-08-29 12:00 UTC"
        
        # Single opportunity
        single_item = [{
            "title": "Implement Zod schema",
            "repo": "stellar/validator",
            "comments": 3,
            "updated_at": "2026-08-29T11:00:00Z",
            "url": "https://github.com/stellar/validator/issues/50"
        }]
        title_1, body_1 = format_github_issue_content(single_item, now_str)
        self.assertEqual(title_1, "🎯 Bounty Alert: 1 New Opportunity found")
        self.assertIn("#### 1. [Implement Zod schema](https://github.com/stellar/validator/issues/50)", body_1)
        self.assertIn("- **Repository:** [stellar/validator](https://github.com/stellar/validator)", body_1)

        # Reusable alias check
        alias_title, alias_body = build_github_issue_payload(single_item, now_str)
        self.assertEqual(title_1, alias_title)
        self.assertEqual(body_1, alias_body)

        # Multiple opportunities
        multi_items = [
            {
                "title": "Task A",
                "repo": "org/repoA",
                "comments": 0,
                "updated_at": "2026-08-29T10:00:00Z",
                "url": "https://github.com/org/repoA/issues/1"
            },
            {
                "title": "Task B",
                "repo": "org/repoB",
                "comments": 1,
                "updated_at": "2026-08-29T10:30:00Z",
                "url": "https://github.com/org/repoB/issues/2"
            }
        ]
        title_2, body_2 = format_github_issue_content(multi_items, now_str)
        self.assertEqual(title_2, "🎯 Bounty Alert: 2 New Opportunities found")
        self.assertNotIn("Opportunityies", title_2)


if __name__ == "__main__":
    unittest.main()
