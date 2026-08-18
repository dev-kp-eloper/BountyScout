# SPDX-License-Identifier: MIT

# SPDX-License-Identifier: MIT
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

@dataclass
class Opportunity:
    title: str
    reward: int = field(default=0)
    url: str = field(default="")
    date: date = field(default_factory=date.today)

class BountyScout:
    def __init__(self, source: Optional[List] = None) -> None:
        self._items: List[Opportunity] = []
        if source:
            for raw in source:
                self._items.append(Opportunity(
                    title=raw.get("title", "Untitled"),
                    reward=raw.get("reward", 0),
                    url=raw.get("url", "")
                ))

    def report(self, count: int = 7) -> str:
        if not self._items:
            return ""
        limit = min(count, len(self._items)) if count else len(self._items)
        output: List[str] = []
        for i in range(limit):
            output.append(f"[{i + 1}] {self._items[i].title}")
        return "\n".join(output)

def main() -> None:
    raw_feed: List = [
        {"title": "Alpha", "reward": 250},
        {"title": "Beta", "reward": 120},
        {"title": "Gamma", "reward": 50},
    ]
    scout = BountyScout(raw_feed)
    print(scout.report(7))

if __name__ == "__main__":
    main()