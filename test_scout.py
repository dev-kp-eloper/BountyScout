import unittest
from scout_bounties import extract_reward

class TestBountyScout(unittest.TestCase):
    def test_extract_reward(self):
        cases = [
            ("This is a $100 bounty", "Task", "$100"),
            ("Reward: 50 USD", "Fix bug", "50 USD"),
            ("Bounty: 2.5 SOL", "Implement feature", "2.5 SOL"),
            ("No reward here", "Just a task", None),
            ("Title has $500", "$500 Bounty", "$500"),
        ]
        for body, title, expected in cases:
            with self.subTest(body=body, title=title):
                self.assertEqual(extract_reward(body, title), expected)

if __name__ == "__main__":
    unittest.main()
