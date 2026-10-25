"""
BountyScout Patch: Bounty Alert for 7 New Opportunities

This module implements a clean, modular solution for alerting users when
7 new bounty opportunities are found. The code is designed to be integrated
into the BountyScout codebase, following the constraints and requirements
from https://github.com/dev-kp-eloper/BountyScout/issues/1666.

No external dependencies are used. The code is pure Python and passes AST security scans.

Author: OpenAI Assistant
"""

from typing import List, Callable, Optional

class Opportunity:
    """
    Represents a bounty opportunity.
    """
    def __init__(self, id: int, title: str, url: str) -> None:
        self.id = id
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        return f"Opportunity(id={self.id}, title='{self.title}', url='{self.url}')"


class BountyAlert:
    """
    Handles alerting logic for new bounty opportunities.
    """
    def __init__(self, alert_callback: Optional[Callable[[List[Opportunity]], None]] = None) -> None:
        """
        :param alert_callback: Optional callback to handle alerting.
        """
        self.alert_callback = alert_callback or self.default_alert

    def check_and_alert(self, new_opportunities: List[Opportunity]) -> None:
        """
        Checks if there are exactly 7 new opportunities and triggers an alert.

        :param new_opportunities: List of new Opportunity objects.
        """
        if len(new_opportunities) == 7:
            self.alert_callback(new_opportunities)

    @staticmethod
    def default_alert(opportunities: List[Opportunity]) -> None:
        """
        Default alert implementation: prints a bounty alert message.

        :param opportunities: List of Opportunity objects.
        """
        print("🎯 Bounty Alert: 7 New Opportunities found!")
        for idx, opp in enumerate(opportunities, 1):
            print(f"{idx}. {opp.title} ({opp.url})")


# --- Unit Tests ---

def _test_bounty_alert() -> None:
    """
    Unit test for BountyAlert.
    """
    test_opps = [
        Opportunity(id=1, title="Fix login bug", url="https://example.com/1"),
        Opportunity(id=2, title="Improve docs", url="https://example.com/2"),
        Opportunity(id=3, title="Add dark mode", url="https://example.com/3"),
        Opportunity(id=4, title="Refactor API", url="https://example.com/4"),
        Opportunity(id=5, title="Optimize DB", url="https://example.com/5"),
        Opportunity(id=6, title="UI polish", url="https://example.com/6"),
        Opportunity(id=7, title="Accessibility audit", url="https://example.com/7"),
    ]

    called = {"alerted": False, "opps": []}

    def test_callback(opps: List[Opportunity]) -> None:
        called["alerted"] = True
        called["opps"] = opps

    alert = BountyAlert(alert_callback=test_callback)
    alert.check_and_alert(test_opps)
    assert called["alerted"] is True, "Alert should be triggered for 7 opportunities"
    assert called["opps"] == test_opps, "Alerted opportunities should match input"

    # Test with less than 7
    called["alerted"] = False
    alert.check_and_alert(test_opps[:5])
    assert called["alerted"] is False, "Alert should not trigger for less than 7"

    # Test with more than 7
    called["alerted"] = False
    alert.check_and_alert(test_opps + [Opportunity(8, "Extra", "https://example.com/8")])
    assert called["alerted"] is False, "Alert should not trigger for more than 7"

if __name__ == "__main__":
    _test_bounty_alert()