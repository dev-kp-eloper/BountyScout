import unittest

from scout_bounties import opportunity_label


class OpportunityLabelTests(unittest.TestCase):
    def test_singular_label(self):
        self.assertEqual(opportunity_label(1), "opportunity")

    def test_plural_label(self):
        self.assertEqual(opportunity_label(18), "opportunities")


if __name__ == "__main__":
    unittest.main()
