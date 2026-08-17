```python
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum, auto
from datetime import datetime, timedelta
import random
from collections import defaultdict
import json

class BountyStatus(Enum):
    ACTIVE = "active"
    CLAIMED = "claimed"
    EXPIRED = "expired"
    PENDING = "pending"

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

@dataclass
class Bounty:
    name: str
    platform: str
    reward: float
    deadline: datetime
    difficulty: Difficulty
    tags: List[str]
    url: str
    claimed_by: Optional[str] = None
    claimed_at: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        return datetime.now() > self.deadline

    def get_remaining_days(self) -> int:
        return (self.deadline - datetime.now()).days

    def __str__(self) -> str:
        return f"{self.name} ({self.platform}) - ${self.reward}"


class BountyCollector:
    def __init__(self, platform: str = "multi", auto_refresh: bool = True):
        self.platform = platform
        self.auto_refresh = auto_refresh
        self.bounties: Dict[str, Bounty] = {}
        self.callbacks: List[Callable[[Bounty], Any]] = []
        
    def register_callback(self, callback: Callable[[Bounty], Any]) -> None:
        if not callable(callback):
            raise TypeError("Callback must be a callable")
        self.callbacks.append(callback)
    
    def add_bounty(self, name: str, **kwargs) -> Bounty:
        bounty = Bounty(name=name, **kwargs)
        self.bounties[name] = bounty
        self._trigger_callbacks(bounty)
        return bounty
    
    def _trigger_callbacks(self, bounty: Bounty) -> None:
        for callback in self.callbacks:
            try:
                result = callback(bounty)
            except Exception as e:
                print(f"Callback error for {bounty.name}: {e}")
    
    def filter_by_difficulty(self, difficulty: Difficulty) -> List[Bounty]:
        return [b for b in self.bounties.values() if b.difficulty == difficulty]
    
    def filter_by_deadline(self, days: int) -> List[Bounty]:
        cutoff = datetime.now() + timedelta(days=days)
        return [b for b in self.bounties.values() if datetime.now() <= b.deadline <= cutoff]
    
    def get_active_bounties(self) -> List[Bounty]:
        return [b for b in self.bounties.values() if b.difficulty != Difficulty.EXPERT or b.is_expired()]
    
    def update_deadline(self, name: str, new_deadline: datetime) -> Optional[Bounty]:
        if name in self.bounties:
            self.bounties[name].deadline = new_deadline
            self._trigger_callbacks(self.bounties[name])
            return self.bounties[name]
        return None
    
    def claim_bounty(self, name: str, claimer: str) -> Optional[Bounty]:
        bounty = self.bounties.get(name)
        if bounty and not bounty.claimed_by:
            bounty.claimed_by = claimer
            bounty.claimed_at = datetime.now()
            self._trigger_callbacks(bounty)
            return bounty
        return bounty
    
    def generate_summary(self) -> Dict[str, Any]:
        active = [b for b in self.bounties.values() if not b.is_expired()]
        total_value = sum(b.reward for b in active)
        by_difficulty = defaultdict(list)
        
        for b in self.bounties.values():
            by_difficulty[b.difficulty.value].append(b)
        
        return {
            "platform": self.platform,
            "total": len(self.bounties),
            "active": len(active),
            "total_value": round(total_value, 2),
            "by_difficulty": dict(by_difficulty),
            "top_rewards": sorted([b for b in active if b.reward > 0], key=lambda x: x.reward, reverse=True)[:5]
        }
    
    def load_from_json(self, filepath: str) -> None:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for name, bdata in data.items():
                    if name in self.bounties:
                        self.update_deadline(name, datetime.fromisoformat(bdata['deadline']))
                    else:
                        bdata['deadline'] = datetime.fromisoformat(bdata['deadline'])
                        self.bounties[name] = Bounty(**bdata)
                        self._trigger_callbacks(self.bounties[name])
        except FileNotFoundError:
            print(f"File not found: {filepath}")
    
    def save_to_json(self, filepath: str) -> None:
        data = {name: {
            'name': b.name, 'platform': b.platform, 'reward': b.reward,
            'deadline': b.deadline.isoformat(), 'difficulty': b.difficulty.value,
            'tags': b.tags, 'url': b.url, 'claimed_by': b.claimed_by,
            'claimed_at': b.claimed_at.isoformat() if b.claimed_at else None
        } for name, b in self.bounties.items()}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
```