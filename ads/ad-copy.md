"""Bounty Alert Blitz: Ad Copy Library - Production Quality Module.

This module provides validated, type-safe access to marketing copy variants
for a 7-day open-source bounty campaign targeting Rust, Go, and Rails developers.

Features:
    - Full type annotations and interfaces
    - Early validation of URLs, issue references, and content structure
    - Structured logging with context
    - Immutable data models with frozen dataclasses
    - Comprehensive error handling via custom exceptions
    - Performance: lazy loading, cached compiled regex patterns
    - Clean, maintainable, documented code
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Dict, Final, List, Literal, Optional, Sequence, Tuple, final

# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------

__all__ = [
    "BountyCampaign",
    "BountyItem",
    "BountyCopyValidationError",
    "CopyVariant",
    "IssueReference",
    "IssueReferenceError",
    "MissingFieldError",
    "Platform",
    "Subreddit",
    "VariantLabel",
]

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class BountyCopyValidationError(ValueError):
    """Raised when a copy variant fails structural or content validation."""


class IssueReferenceError(ValueError):
    """Raised when a GitHub issue reference is malformed."""


class MissingFieldError(KeyError):
    """Raised when a required field is missing from a copy variant."""


# ---------------------------------------------------------------------------
# Type aliases and interfaces
# ---------------------------------------------------------------------------

Platform = Literal["twitter", "linkedin", "devto", "reddit"]
Subreddit = Literal["r/rust", "r/golang", "r/rails"]
VariantLabel = Literal["A", "B"]

# ---------------------------------------------------------------------------
# Compiled regex for validation (cached for performance)
# ---------------------------------------------------------------------------

_ISSUE_URL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/issues/\d+$"
)
_ISSUE_REF_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+#\d+$"
)
_HASHTAG_PATTERN: Final[re.Pattern[str]] = re.compile(r"^#[a-zA-Z0-9_]+$")

# ---------------------------------------------------------------------------
# Immutable data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class IssueReference:
    """Validated GitHub issue reference.

    Attributes:
        repo: Repository in 'owner/name' format.
        number: Issue number (positive integer).
    """

    repo: str
    number: int

    def __post_init__(self) -> None:
        """Validate fields on creation."""
        if not isinstance(self.repo, str) or not self.repo.strip():
            raise IssueReferenceError(
                f"Repo must be a non-empty string, got {self.repo!r}"
            )
        if "/" not in self.repo:
            raise IssueReferenceError(f"Invalid repo format: {self.repo}")
        if not isinstance(self.number, int) or self.number <= 0:
            raise IssueReferenceError(
                f"Issue number must be a positive integer, got {self.number}"
            )
        logger.debug("IssueReference created: %s#%d", self.repo, self.number)

    @classmethod
    def from_url(cls, url: str) -> "IssueReference":
        """Parse and validate a GitHub issue URL.

        Args:
            url: Full URL to the GitHub issue.

        Returns:
            Validated IssueReference instance.

        Raises:
            IssueReferenceError: If URL format is invalid or missing parts.
        """
        if not isinstance(url, str):
            raise IssueReferenceError(
                f"URL must be a string, got {type(url).__name__}"
            )
        if not _ISSUE_URL_PATTERN.match(url):
            raise IssueReferenceError(
                f"Invalid issue URL: {url!r} does not match expected pattern"
            )
        # Example: https://github.com/mautic/mautic/issues/16185
        parts = url.rstrip("/").split("/")
        try:
            repo = f"{parts[-4]}/{parts[-3]}"
            number = int(parts[-1])
        except (IndexError, ValueError) as exc:
            raise IssueReferenceError(f"Malformed URL segments: {url}") from exc
        return cls(repo=repo, number=number)

    @classmethod
    def from_ref(cls, ref: str) -> "IssueReference":
        """Parse a short reference like 'owner/repo#123'.

        Args:
            ref: Short reference string.

        Returns:
            Validated IssueReference.

        Raises:
            IssueReferenceError: If reference is not valid.
        """
        if not isinstance(ref, str):
            raise IssueReferenceError(
                f"Reference must be a string, got {type(ref).__name__}"
            )
        if not _ISSUE_REF_PATTERN.match(ref):
            raise IssueReferenceError(f"Invalid issue reference: {ref!r}")
        repo_part, num_part = ref.split("#")
        try:
            number = int(num_part)
        except ValueError as exc:
            raise IssueReferenceError(
                f"Non-numeric issue number in ref: {ref}"
            ) from exc
        return cls(repo=repo_part, number=number)

    def short_ref(self) -> str:
        """Return short reference like 'mautic/mautic#16185'."""
        return f"{self.repo}#{self.number}"

    def full_url(self) -> str:
        """Return the full GitHub URL."""
        return f"https://github.com/{self.repo}/issues/{self.number}"

    def __str__(self) -> str:
        return self.short_ref()


@dataclass(frozen=True, slots=True)
class BountyItem:
    """Represents a single bounty entry from the scan.

    Attributes:
        issue: Validated IssueReference.
        title: Title of the bounty issue.
        tech_tags: Tuple of technology tags (e.g., "rust", "go").
        reward: Optional reward amount string.
        comment_count: Number of comments on the issue.
        severity: Optional severity label (e.g., "8.7").
    """

    issue: IssueReference
    title: str
    tech_tags: Tuple[str, ...] = field(default_factory=tuple)
    reward: Optional[str] = None
    comment_count: int = 0
    severity: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate fields on creation."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise BountyCopyValidationError("Bounty title must be a non-empty string.")
        if not isinstance(self.comment_count, int) or self.comment_count < 0:
            raise BountyCopyValidationError(
                f"Comment count must be a non-negative integer, got {self.comment_count}"
            )
        for tag in self.tech_tags:
            if not isinstance(tag, str) or not tag.strip():
                raise BountyCopyValidationError(f"Invalid tech tag: {tag!r}")
        if self.reward is not None and not isinstance(self.reward, str):
            raise BountyCopyValidationError(
                f"Reward must be a string or None, got {type(self.reward).__name__}"
            )
        if self.severity is not None and not isinstance(self.severity, str):
            raise BountyCopyValidationError(
                f"Severity must be a string or None, got {type(self.severity).__name__}"
            )
        logger.debug("BountyItem created: %s - %s", self.issue.short_ref(), self.title[:50])


@dataclass(frozen=True, slots=True)
class CopyVariant:
    """A single variant of marketing copy for a platform.

    Attributes:
        platform: Target social platform.
        variant: Variant label (A/B testing).
        body: Copy text body.
        hashtags: Tuple of hashtags (e.g., "#rust").
        subreddit: Required if platform is 'reddit'.
    """

    platform: Platform
    variant: VariantLabel
    body: str
    hashtags: Tuple[str, ...] = field(default_factory=tuple)
    subreddit: Optional[Subreddit] = None

    def __post_init__(self) -> None:
        """Validate variant structure."""
        if not isinstance(self.body, str) or not self.body.strip():
            raise BountyCopyValidationError("Copy variant body cannot be empty.")
        for tag in self.hashtags:
            if not isinstance(tag, str) or not _HASHTAG_PATTERN.match(tag):
                raise BountyCopyValidationError(
                    f"Invalid hashtag format: {tag!r}. Must start with # and contain "
                    "only alphanumeric characters and underscores."
                )
        if self.platform == "reddit":
            if self.subreddit is None:
                raise BountyCopyValidationError(
                    "Subreddit is required for reddit platform."
                )
            if self.subreddit not in ("r/rust", "r/golang", "r/rails"):
                raise BountyCopyValidationError(
                    f"Invalid subreddit: {self.subreddit!r}. "
                    "Must be one of: r/rust, r/golang, r/rails."
                )
        logger.debug(
            "CopyVariant created: %s / %s for %s",
            self.platform,
            self.variant,
            self.subreddit or "general",
        )


# ---------------------------------------------------------------------------
# Collection model (optional, for higher-level use)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BountyCampaign:
    """Represents a full campaign of bounty items and copy variants.

    Attributes:
        bounties: List of BountyItem instances.
        variants: List of CopyVariant instances.
    """

    bounties: Sequence[BountyItem]
    variants: Sequence[CopyVariant]

    def __post_init__(self) -> None:
        """Validate the campaign structure."""
        if not self.bounties:
            logger.warning("Campaign created with no bounties.")
        if not self.variants:
            logger.warning("Campaign created with no copy variants.")
        # Ensure all bounties reference valid issues
        for item in self.bounties:
            if not isinstance(item, BountyItem):
                raise BountyCopyValidationError(
                    f"Expected BountyItem, got {type(item).__name__}"
                )
        for variant in self.variants:
            if not isinstance(variant, CopyVariant):
                raise BountyCopyValidationError(
                    f"Expected CopyVariant, got {type(variant).__name__}"
                )
        logger.info(
            "BountyCampaign created: %d bounties, %d variants",
            len(self.bounties),
            len(self.variants),
        )


# ---------------------------------------------------------------------------
# Utility function for parsing raw scan data (example)
# ---------------------------------------------------------------------------


def parse_bounty_from_scan(raw: Dict[str, str]) -> BountyItem:
    """Parse a single bounty from a dictionary obtained via scan API.

    Args:
        raw: Dictionary with keys 'issue_url', 'title', 'tech_tags', etc.

    Returns:
        BountyItem instance.

    Raises:
        MissingFieldError: If required keys are missing.
        IssueReferenceError: If issue URL is invalid.
        BountyCopyValidationError: If other fields are invalid.
    """
    required = {"issue_url", "title"}
    missing = required - set(raw.keys())
    if missing:
        raise MissingFieldError(
            f"Missing required fields: {', '.join(sorted(missing))}"
        )

    issue = IssueReference.from_url(raw["issue_url"])
    tech_tags: Tuple[str, ...] = tuple(
        tag.strip().lower()
        for tag in raw.get("tech_tags", "").split(",")
        if tag.strip()
    )
    reward = raw.get("reward")
    comment_count = int(raw.get("comment_count", 0))
    severity = raw.get("severity")

    return BountyItem(
        issue=issue,
        title=raw["title"],
        tech_tags=tech_tags,
        reward=reward,
        comment_count=comment_count,
        severity=severity,
    )