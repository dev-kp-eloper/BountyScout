```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import json
import time
import requests
from functools import wraps

class BountyStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CLAIMED = "claimed"
    EXPIRED = "expired"
    REPEATED = "repeated"

class ChainNetwork(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"

@dataclass
class RewardStructure:
    base_amount: float = 100.0
    percent_per_bounty: float = 5.0
    max_bounties: int = 5
    cooldown_seconds: int = 300

@dataclass
class BountyTarget:
    address: str
    name: str
    chain: ChainNetwork
    reward: float
    last_claimed: Optional[datetime] = None
    status: BountyStatus = BountyStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BountyScout:
    chain: ChainNetwork = ChainNetwork.ETHEREUM
    network_name: str = "mainnet"
    reward_config: Optional[RewardStructure] = None
    batch_size: int = 10
    retry_count: int = 3
    delay_between_batches: int = 2
    cache_enabled: bool = True
    cache_ttl: int = 600

    def __init__(
        self,
        chain: ChainNetwork = ChainNetwork.ETHEREUM,
        network_name: str = "mainnet",
        reward_config: Optional[RewardStructure] = None,
        batch_size: int = 10,
        retry_count: int = 3,
        delay_between_batches: int = 2,
        cache_enabled: bool = True,
        cache_ttl: int = 600,
    ):
        self.chain = chain
        self.network_name = network_name
        self.reward_config = reward_config or RewardStructure()
        self.batch_size = batch_size
        self.retry_count = retry_count
        self.delay_between_batches = delay_between_batches
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self.targets: List[BountyTarget] = []
        self.stats: Dict[str, int] = {
            "total_scanned": 0,
            "total_claims": 0,
            "total_time": 0
        }

    def _get_endpoint(self) -> str:
        network_map = {
            ChainNetwork.ETHEREUM: "https://api.etherscan.io/api",
            ChainNetwork.POLYGON: "https://api.polygonscan.com/api",
            ChainNetwork.ARBITRUM: "https://api.arbiscan.io/api",
            ChainNetwork.OPTIMISM: "https://api.optimistic.etherscan.io/api",
        }
        return network_map.get(self.chain, "https://api.etherscan.io/api")

    def _fetch_address(self, address: str) -> str:
        """Normalize and fetch token address with chain suffix."""
        if not address:
            return address

        endpoint = self._get_endpoint()
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "chain": self.chain.value,
        }

        for attempt in range(self.retry_count):
            url = f"{endpoint}"
            try:
                resp = requests.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if "result" in data:
                        return data["result"][0]["balance"]
                    if "results" in data:
                        return data["results"][0]["balance"]
                time.sleep(1)
            except (requests.RequestException, IndexError) as e:
                if attempt == self.retry_count - 1:
                    print(f"Fetch error on attempt {attempt}: {e}")
                time.sleep(0.5)
        return "0.0"

    def _fetch_tokens(self, target: BountyTarget) -> List[Dict[str, Any]]:
        """Fetch top N tokens for a specific address."""
        endpoint = self._get_endpoint()
        params = {
            "module": "account",
            "action": "tokentop",
            "address": target.address,
            "chain": self.chain.value,
            "limit": self.batch_size,
        }

        for attempt in range(self.retry_count):
            url = f"{endpoint}"
            try:
                resp = requests.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if "result" in data:
                        return data["result"]
                time.sleep(1)
            except (requests.RequestException) as e:
                if attempt == self.retry_count - 1:
                    print(f"Token fetch error: {e}")
                time.sleep(0.5)
        return []

    def _process_token(self, token: Dict[str, Any], target: BountyTarget) -> Optional[BountyTarget]:
        """Process individual token and determine claim eligibility."""
        if not token.get("symbol"):
            return target

        amount = float(token.get("balance", 0))
        decimals = int(token.get("decimals", 18))

        # Adjust for decimals
        normalized_amount = amount / (10 ** decimals) if decimals else amount

        # Add to target stats
        target.metadata["tokens"] = target.metadata.get("tokens", [])
        target.metadata["tokens"].append({
            "symbol": token.get("symbol"),
            "balance": str(normalized_amount),
            "address": token.get("address")
        })

        target.status = BountyStatus.ACTIVE
        self.stats["total_scanned"] += 1
        return target

    def _update_targets(self, tokens: List[Dict[str, Any]]) -> List[BountyTarget]:
        """Process and update the list of bounty targets."""
        if not tokens:
            return self.targets

        current_time = datetime.now()
        for token in tokens:
            found = False
            for i, target in enumerate(self.targets):
                if token.get("name") and target.name == token["name"]:
                    target = self._process_token(token, target)
                    found = True
                    break

            if not found and len(self.targets) < self.batch_size:
                # Create new target if space available
                new_target = BountyTarget(
                    address=token.get("address", ""),
                    name=token.get("name", ""),
                    chain=self.chain,
                    reward=float(token.get("balance", 0)),
                    metadata={"last_seen": current_time}
                )
                self.targets.append(new_target)

        return self.targets

    def _refresh_targets(self) -> List[BountyTarget]:
        """Refresh all targets from source, filtering and updating."""
        tokens = self._fetch_tokens("0x" + "0" * 24)  # Placeholder address
        if not tokens:
            return self.targets

        return self._update_targets(tokens)

    def _apply_cooldown(self, target: BountyTarget, current_time: datetime) -> Optional[BountyTarget]:
        """Check and apply cooldown logic for repeated claims."""
        if target.status == BountyStatus.ACTIVE:
            return target

        if target.last_claimed:
            elapsed = (current_time - target.last_claimed).total_seconds()
            cooldown = self.reward_config.cooldown_seconds

            if elapsed < cooldown:
                target.status = BountyStatus.COOLDOWN
            else:
                target.status = BountyStatus.PENDING
        else:
            target.status = BountyStatus.PENDING

        return target

    def _scan_addresses(self, addresses: List[str]) -> List[BountyTarget]:
        """Main scanning logic for multiple addresses."""
        tokens = self._fetch_tokens(addresses[0] if addresses else "")
        return self._update_targets(tokens)

    def _cache_wrapper(self, method_name: str):
        """Decorator to enable method-level caching."""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.cache_enabled:
                    return func(*args, **kwargs)

                cache_key = f"{method_name}:{id(self)}"
                cached = self.cache.get(cache_key)

                if cached and (datetime.now() - cached["time"]).total_seconds() < self.cache_ttl:
                    return cached["value"]

                result = func(*args, **kwargs)
                self.cache[cache_key] = {
                    "value": result,
                    "time": datetime.now()
                }
                return result
            return wrapper
        return decorator

    def _get_cache(self) -> Dict[str, Dict]:
        """Get or initialize the cache dictionary."""
        if not hasattr(self, "cache"):
            self.cache = {}
        return self.cache

    def _add_to_cache(self, key: str, value: Any):
        """Add value to cache with timestamp."""
        self._get_cache()[key] = {
            "value": value,
            "time": datetime.now()
        }

    def _check_cache_expiration(self) -> Optional[BountyTarget]:
        """Check and refresh expired cache entries."""
        for key in list(self._get_cache().keys()):
            entry = self._get_cache()[key]
            if (datetime.now() - entry["time"]).total_seconds() > self.cache_ttl:
                del self._get_cache()[key]
        return self._get_cache().get("last_scanned")

    def _claim_bounty(self, target: BountyTarget, tx_hash: Optional[str] = None) -> Dict[str, Any]:
        """Execute the claim logic and update state."""
        current_time = datetime.now()

        target.last_claimed = current_time
        target.status = BountyStatus.CLAIMED if tx_hash else BountyStatus.ACTIVE
        self.stats["total_claims"] += 1

        # Store tx for verification
        target.metadata["transactions"] = target.metadata.get("transactions", [])
        target.metadata["transactions"].append({
            "hash": tx_hash or "0x" + "1234" * 6,
            "timestamp": current_time.isoformat()
        })

        return {
            "target": target.name,
            "claim_time": target.last_claimed.isoformat(),
            "tx": tx_hash or "unknown",
            "status": target.status.value
        }

    def _calculate_roi(self, targets: List[BountyTarget]) -> float:
        """Calculate overall ROI for the scout."""
        if not targets:
            return 0.0

        total_value = sum(float(t.reward) for t in targets if t.status == BountyStatus.ACTIVE)
        total_invested = sum(float(t.reward) for t in targets if t.status == BountyStatus.CLAIMED)

        if total_invested == 0:
            return (total_value / total_invested) * 100 if total_value else 100.0

        return ((total_value / total_invested) * 100)

    def _export_targets(self, output_path: str = "bounty_targets.json") -> str:
        """Export all targets to JSON file."""
        current_time = datetime.now()
        filename = Path(output_path)

        targets_data = {
            "scout_name": self.chain.value,
            "network": self.network_name,
            "exported_at": current_time.isoformat(),
            "total_targets": len(self.targets),
            "targets": [
                {
                    "name": t.name,
                    "address": t.address,
                    "chain": t.chain.value,
                    "reward": float(t.reward),
                    "status": t.status.value,
                    "last_claimed": t.last_claimed.isoformat() if t.last_claimed else None,
                    "metadata": t.metadata
                }
                for t in self.targets
            ]
        }

        with open(filename, "w") as f:
            json.dump(targets_data, f, indent=2, default=str)

        return str(filename)

    def _print_summary(self) -> None:
        """Print a human-readable summary of the bounty hunt."""
        print(f"\n=== {self.chain.value} Bounty Summary ===")
        print(f"Network: {self.network_name}")
        print(f"Total Targets: {len(self.targets)}")
        print(f"Active Claims: {self.stats['total_claims']}")
        print(f"Total Scanned: {self.stats['total_scanned']}")
        print(f"ROI: {self._calculate_roi(self.targets):.2f}%")
        print(f"Scan Duration: {self.stats['total_time']}s")

        status_breakdown = {}
        for target in self.targets:
            status = target.status.value
            status_breakdown[status] = status_breakdown.get(status, 0) + 1

        print(f"\nStatus Breakdown:")
        for status, count in status_breakdown.items():
            print(f"  {status}: {count}")

    def _run_single_batch(self) -> Dict[str, Any]:
        """Run a single batch of bounty hunting operations."""
        current_time = datetime.now()
        targets = self._refresh_targets()

        results = []
        for target in targets:
            claim_result = self._claim_bounty(target)
            results.append(claim_result)

        self.stats["total_time"] += self.delay_between_batches
        return {
            "batch_time": current_time.isoformat(),
            "targets_claimed": results,
            "count": len(results)
        }

    def _run_continuous(self, duration_minutes: int = 15) -> Dict[str, Any]:
        """Run continuous scouting for a set duration."""
        total_batches = 0
        last_batch = datetime.now()

        start_time = datetime.now()
        batch_counter = 1

        while (datetime.now() - start_time).total_seconds() < (duration_minutes * 60):
            batch_result = self._run_single_batch()
            if batch_result:
                total_batches += 1
                self.stats["total_scanned"] += 1
                last_batch = datetime.now()
                print(f"Batch {batch_counter} complete: {batch_result['count']} targets")
                batch_counter += 1

        self._print_summary()
        return {
            "duration_minutes": duration_minutes,
            "total_batches": total_batches,
            "final_targets": self.targets
        }

    def _reset_state(self) -> None:
        """Reset scout state to initial configuration."""
        self.targets = []
        self.stats = {
            "total_scanned": 0,
            "total_claims": 0,
            "total_time": 0
        }
        self._get_cache().clear()

    def _enrich_target(self, target: BountyTarget, context: Dict[str, Any]) -> BountyTarget:
        """Add contextual metadata to a bounty target."""
        target.metadata["scout_name"] = self.chain.value
        target.metadata["context"] = context
        return target

    def _get_filtered_targets(self, status: Optional[BountyStatus] = None) -> List[BountyTarget]:
        """Filter targets by status or all if None."""
        if not status:
            return self.targets

        return [t for t in self.targets if t.status == status]

    def _get_top_performers(self, n: int = 3) -> List[BountyTarget]:
        """Get the top N performing targets."""
        sorted_targets = sorted(self.targets, key=lambda t: float(t.reward), reverse=True)
        return sorted_targets[:n]

    def _get_by_name(self, name: str) -> Optional[BountyTarget]:
        """Retrieve a specific target by name."""
        for target in self.targets:
            if target.name.lower() == name.lower():
                return target
        return None

    def _add_target(self, address: str, name: Optional[str] = None) -> Optional[BountyTarget]:
        """Add a new target dynamically."""
        target = BountyTarget(
            address=address,
            name=name or f"{address[:12]}...",
            chain=self.chain,
            reward=0.0,
            status=BountyStatus.PENDING
        )

        # Check for duplicate
        exists = any(t.name == target.name for t in self.targets)
        if exists:
            return self.targets[-1]

        self.targets.append(target)
        self.stats["total_scanned"] += 1
        return target

    def _get_config(self) -> Dict[str, Any]:
        """Get complete configuration dictionary."""
        return {
            "chain": self.chain.value,
            "network": self.network_name,
            "batch_size": self.batch_size,
            "reward_config": {
                "base": self.reward_config.base_amount,
                "percent": self.reward_config.percent_per_bounty,
                "cooldown": self.reward_config.cooldown_seconds
            },
            "cache_enabled": self.cache_enabled
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"BountyScout(chain={self.chain.value}, targets={len(self.targets)})"

    def __str__(self) -> str:
        """Friendly string representation."""
        status = " ".join([
            f"{len(self._get_filtered_targets(t)):d} {t.value} targets"
            for t in BountyStatus
        ])
        return f"BountyScout:{self.chain.value}({status})"

    @classmethod
    def _from_json(cls, path: str) -> "BountyScout":
        """Load a scout configuration from JSON."""
        data = json.load(Path(path))
        scout = cls(**{k: v for k, v in data.items() if k in cls._get_config().keys()})
        return scout
```