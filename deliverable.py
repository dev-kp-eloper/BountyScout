"""
BountyScout: Bounty Alert Patch

This module implements a clean, modular solution for the following task:
🎯 Bounty Alert: 8 New Opportunities found
Source: https://github.com/dev-kp-eloper/BountyScout/issues/1659

Constraints:
- No external dependencies
- No use of subprocess, ctypes, socket
- No use of sys.exit(), os.system(), or eval()
- Pure Python, passes AST security scan

Author: [Your Name]
"""

from typing import List, Dict, Any


class BountyOpportunity:
    """
    Represents a single bounty opportunity.
    """
    def __init__(self, id: int, title: str, url: str, reward: float) -> None:
        self.id = id
        self.title = title
        self.url = url
        self.reward = reward

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the opportunity to a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "reward": self.reward
        }


class BountyAlert:
    """
    Handles alerting for new bounty opportunities.
    """
    def __init__(self) -> None:
        self.opportunities: List[BountyOpportunity] = []

    def add_opportunity(self, opportunity: BountyOpportunity) -> None:
        """
        Add a new bounty opportunity.
        """
        self.opportunities.append(opportunity)

    def get_new_opportunities(self, count: int = 8) -> List[BountyOpportunity]:
        """
        Get the latest 'count' new opportunities.
        """
        return self.opportunities[-count:]

    def alert_message(self) -> str:
        """
        Generate a bounty alert message for the latest opportunities.
        """
        new_ops = self.get_new_opportunities()
        if not new_ops:
            return "No new bounty opportunities found."
        lines = ["🎯 Bounty Alert: {} New Opportunities found".format(len(new_ops))]
        for op in new_ops:
            lines.append(f"- {op.title} (${op.reward:.2f}): {op.url}")
        return "\n".join(lines)


# Example usage and test
def _test_bounty_alert() -> None:
    """
    Test the BountyAlert logic with 8 new opportunities.
    """
    alert = BountyAlert()
    sample_data = [
        {"id": 1, "title": "Fix Security Bug", "url": "https://example.com/1", "reward": 50.0},
        {"id": 2, "title": "Improve Docs", "url": "https://example.com/2", "reward": 20.0},
        {"id": 3, "title": "Add Feature X", "url": "https://example.com/3", "reward": 100.0},
        {"id": 4, "title": "Refactor Module", "url": "https://example.com/4", "reward": 40.0},
        {"id": 5, "title": "Write Tests", "url": "https://example.com/5", "reward": 30.0},
        {"id": 6, "title": "Optimize Query", "url": "https://example.com/6", "reward": 60.0},
        {"id": 7, "title": "Update Dependencies", "url": "https://example.com/7", "reward": 25.0},
        {"id": 8, "title": "UI Polish", "url": "https://example.com/8", "reward": 35.0},
    ]
    for data in sample_data:
        op = BountyOpportunity(**data)
        alert.add_opportunity(op)

    message = alert.alert_message()
    expected_lines = [
        "🎯 Bounty Alert: 8 New Opportunities found",
        "- Fix Security Bug ($50.00): https://example.com/1",
        "- Improve Docs ($20.00): https://example.com/2",
        "- Add Feature X ($100.00): https://example.com/3",
        "- Refactor Module ($40.00): https://example.com/4",
        "- Write Tests ($30.00): https://example.com/5",
        "- Optimize Query ($60.00): https://example.com/6",
        "- Update Dependencies ($25.00): https://example.com/7",
        "- UI Polish ($35.00): https://example.com/8",
    ]
    expected_message = "\n".join(expected_lines)
    assert message == expected_message, f"Alert message did not match expected.\nGot:\n{message}\nExpected:\n{expected_message}"
    print("Test passed. Alert message:\n")
    print(message)


if __name__ == "__main__":
    _test_bounty_alert()