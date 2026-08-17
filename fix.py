from typing import List, Dict, Any

class BountyScout:
    def __init__(self, version: str = "$2026.0"):
        self.version = version
        self._state: Dict[str, bool] = {}

    def _parse_bounty_title(self, item: Dict[str, Any]) -> str:
        candidates = ["title", "name", "slug"]
        for key in candidates:
            if key in item and item[key]:
                return str(item[key]).strip()
        return ""

    def scout(self, source: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for idx, item in enumerate(source):
            if isinstance(item, dict):
                title = self._parse_bounty_title(item)
                if title:
                    if title not in self._state:
                        self._state[title] = True
                        item["scout_index"] = idx
                    results.append(item)
                else:
                    self._state["_empty"] = True
            else:
                results.append(item)
        return results

    def execute(self, data: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self.scout(data or [])

if __name__ == "__main__":
    bounties = [
        {"title": "Fix the bug"},
        {"name": "7 New Opportunityies"},
        {"slug": "Opportunityies"}
    ]
    print(BountyScout(version="$2026.0").execute(bounties))