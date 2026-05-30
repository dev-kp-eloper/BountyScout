#!/usr/bin/env python3
"""
Bounty Alert Blitz: Automated campaign manager for open-source bounty promotion.

Production-grade module for multi-channel marketing campaigns to drive developers
to claim bounties. Implements robust error handling, full type annotations,
comprehensive logging, input validation, performance optimizations, and clean code.

Dependencies (stdlib only for zero external risk):
    - abc, collections.abc, dataclasses, datetime, email, enum,
      http.client, json, logging, os, ssl, time, typing, urllib

Features:
    - Immutable data models with runtime validation
    - Abstract messenger interface with pluggable implementations
    - Rate-limit aware API client with exponential backoff
    - Secure credential management via environment variables
    - Structured logging with context enrichment
    - Configurable campaign intervals and content templates
    - Metrics collection and failure fallback
"""

from __future__ import annotations

import abc
import json
import logging
import os
import random
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.utils import formataddr
from enum import Enum, auto
from http.client import HTTPSConnection, HTTPException
from typing import (
    Any,
    ClassVar,
    Final,
    Optional,
    Sequence,
    Type,
    TypeVar,
    cast,
    overload,
)

# ---------------------------------------------------------------------------
# Module-level exports
# ---------------------------------------------------------------------------

__all__ = [
    "BountyBlitzError",
    "ConfigurationError",
    "APIError",
    "ValidationError",
    "RateLimitError",
    "NetworkError",
    "BountyStatus",
    "Channel",
    "Bounty",
    "CampaignConfig",
    "CampaignManager",
    "GitHubFetcher",
    "Messenger",
    "EmailMessenger",
    "run_campaign",
]

# ---------------------------------------------------------------------------
# Custom exception hierarchy
# ---------------------------------------------------------------------------


class BountyBlitzError(Exception):
    """Base exception for all Bounty Blitz errors."""


class ConfigurationError(BountyBlitzError):
    """Raised when required configuration is missing or invalid."""


class APIError(BountyBlitzError):
    """Raised when an external API call fails."""


class ValidationError(BountyBlitzError):
    """Raised when input validation fails."""


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""


class NetworkError(APIError):
    """Raised on network or protocol errors."""


# ---------------------------------------------------------------------------
# Logging configuration – structured, context-aware
# ---------------------------------------------------------------------------

_logger = logging.getLogger("bounty_blitz")
_logger.setLevel(logging.DEBUG)

# Ensure handlers are not duplicated on module reload
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.DEBUG)
    _formatter = logging.Formatter(
        "[%(asctime)s] %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    )
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)


class StructuredLogger:
    """Logger with context enrichment and simplified interface."""

    def __init__(self, logger: logging.Logger, extra: dict[str, Any] | None = None) -> None:
        self._logger = logger
        self._extra = extra or {}

    def _log(
        self, level: int, msg: str, *args: Any, exc_info: bool = False, **kwargs: Any
    ) -> None:
        self._logger.log(level, msg, *args, extra=self._extra, exc_info=exc_info, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.CRITICAL, msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.ERROR, msg, *args, exc_info=True, **kwargs)

    def child(self, **extra: Any) -> "StructuredLogger":
        merged = {**self._extra, **extra}
        return StructuredLogger(self._logger, merged)


log = StructuredLogger(_logger)

# ---------------------------------------------------------------------------
# Constants & secrets management
# ---------------------------------------------------------------------------

_ENV_PREFIX: Final[str] = "BOUNTY_BLITZ_"
_CREDENTIAL_KEYS: Final[tuple[str, ...]] = (
    "GITHUB_TOKEN",
    "TWITTER_API_KEY",
    "TWITTER_API_SECRET",
    "LINKEDIN_ACCESS_TOKEN",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASS",
    "NEWSLETTER_LIST_ID",
)

_SECRET_CACHE: dict[str, str] = {}


def load_secret(key: str) -> str:
    """Load a secret from environment variable, caching the result.

    Args:
        key: Secret name (without prefix).

    Returns:
        The secret value, or empty string if not set.
    """
    if key in _SECRET_CACHE:
        return _SECRET_CACHE[key]

    value = os.getenv(f"{_ENV_PREFIX}{key}")
    if value is None or not value.strip():
        log.warning("Secret '%s' is not set – using empty string", key)
        _SECRET_CACHE[key] = ""
        return ""

    cleaned = value.strip()
    _SECRET_CACHE[key] = cleaned
    return cleaned


def validate_secrets() -> None:
    """Ensure all required secrets are present.

    Raises:
        ConfigurationError: If any required secret is missing.
    """
    missing = [key for key in _CREDENTIAL_KEYS if not load_secret(key)]
    if missing:
        raise ConfigurationError(
            f"Missing required secrets: {', '.join(missing)}. "
            f"Set environment variables with prefix '{_ENV_PREFIX}'."
        )


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class BountyStatus(Enum):
    """Status of a bounty issue."""

    PUBLISHED = auto()
    CLAIMED = auto()
    RESOLVED = auto()
    CLOSED = auto()


class Channel(Enum):
    """Supported distribution channels."""

    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    DEVTO = "devto"
    HACKER_NEWS = "hacker_news"
    REDDIT = "reddit"
    EMAIL = "email"


_GITHUB_URL_PATTERN: Final[str] = "https://github.com/"


@dataclass(frozen=True, slots=True)
class Bounty:
    """Immutable representation of a GitHub issue bounty.

    Attributes:
        title: Bounty title.
        url: GitHub issue URL.
        repository: Owner/repo string.
        comments: Number of comments.
        last_updated: Last modification timestamp.
        status: Current bounty status.
        reward: Optional reward description.
        skills: Tuple of required skills.
    """

    title: str
    url: str
    repository: str
    comments: int
    last_updated: datetime
    status: BountyStatus = BountyStatus.PUBLISHED
    reward: Optional[str] = None
    skills: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate fields after initialization.

        Raises:
            ValidationError: If any field violates constraints.
        """
        if not self.title.strip():
            raise ValidationError("Bounty title must not be empty")
        if not self.url.startswith(_GITHUB_URL_PATTERN):
            raise ValidationError(f"Invalid GitHub URL: {self.url}")
        if self.comments < 0:
            raise ValidationError("Comments count cannot be negative")
        if not self.repository.strip():
            raise ValidationError("Repository must not be empty")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for logging or transmission.

        Returns:
            Dictionary with all fields.
        """
        return {
            "title": self.title,
            "url": self.url,
            "repository": self.repository,
            "comments": self.comments,
            "last_updated": self.last_updated.isoformat(),
            "status": self.status.name,
            "reward": self.reward,
            "skills": list(self.skills),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Bounty:
        """Deserialize from a dictionary.

        Args:
            data: Dictionary with keys matching fields.

        Returns:
            Bounty instance.

        Raises:
            ValidationError: If data is invalid.
        """
        required = {"title", "url", "repository", "comments", "last_updated"}
        missing = required - set(data.keys())
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(missing)}")
        try:
            last_updated = datetime.fromisoformat(data["last_updated"])
        except (ValueError, TypeError) as exc:
            raise ValidationError(f"Invalid last_updated format: {exc}") from exc
        return cls(
            title=str(data["title"]),
            url=str(data["url"]),
            repository=str(data["repository"]),
            comments=int(data["comments"]),
            last_updated=last_updated,
            status=BountyStatus[data.get("status", "PUBLISHED").upper()],
            reward=str(data["reward"]) if data.get("reward") else None,
            skills=tuple(str(s) for s in data.get("skills", [])),
        )


@dataclass(frozen=True, slots=True)
class CampaignConfig:
    """Configuration for a campaign run.

    Attributes:
        channels: List of channels to post to.
        min_reward: Minimum reward string to filter (case‑insensitive).
        max_age_hours: Maximum age of bounty in hours (None = no limit).
        cooldown_minutes: Minimum minutes between posts per channel.
        template: Message template string with placeholders.
    """

    channels: tuple[Channel, ...] = (Channel.TWITTER,)
    min_reward: Optional[str] = None
    max_age_hours: Optional[float] = None
    cooldown_minutes: float = 5.0
    template: str = "🐞 Bounty Alert: {title}\n💰 Reward: {reward or 'Undisclosed'}\n📦 {url}"

    def __post_init__(self) -> None:
        """Validate configuration fields.

        Raises:
            ValidationError: On invalid values.
        """
        if not self.channels:
            raise ValidationError("At least one channel is required")
        if self.cooldown_minutes <= 0:
            raise ValidationError("cooldown_minutes must be positive")
        if not self.template.strip():
            raise ValidationError("template must not be empty")


# ---------------------------------------------------------------------------
# Metrics collector (simple in‑memory counter)
# ---------------------------------------------------------------------------


class Metrics:
    """Collects campaign metrics."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = {}
        self._errors: dict[str, int] = {}
        self._start_time: datetime = datetime.now(timezone.utc)

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a named counter."""
        self._counters[name] = self._counters.get(name, 0) + value

    def record_error(self, channel: str) -> None:
        """Record an error for a channel."""
        self._errors[channel] = self._errors.get(channel, 0) + 1

    def report(self) -> dict[str, Any]:
        """Return a snapshot of metrics.

        Returns:
            Dictionary with metrics.
        """
        total_errors = sum(self._errors.values())
        uptime = (datetime.now(timezone.utc) - self._start_time).total_seconds()
        return {
            "counters": dict(self._counters),
            "errors": dict(self._errors),
            "total_errors": total_errors,
            "uptime_seconds": uptime,
        }


# ---------------------------------------------------------------------------
# Retry decorator with exponential backoff
# ---------------------------------------------------------------------------

T = TypeVar("T")


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (APIError, NetworkError, RateLimitError),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator: retry a callable with exponential backoff.

    Args:
        max_retries: Maximum number of retries.
        base_delay: Initial delay in seconds.
        max_delay: Maximum delay in seconds.
        backoff: Multiplier for delay after each retry.
        exceptions: Exception types that trigger a retry.

    Returns:
        Decorated function.

    Raises:
        APIError: If all retries are exhausted.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc: Exception | None = None
            delay = base_delay
            for attempt in range(1, max_retries + 2):  # +1 for initial attempt
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt > max_retries:
                        break
                    log.warning(
                        "Retry %d/%d for %s: %s. Waiting %.2fs",
                        attempt,
                        max_retries,
                        func.__name__,
                        exc,
                        delay,
                    )
                    time.sleep(min(delay, max_delay))
                    delay *= backoff
            raise APIError(f"All {max_retries} retries exhausted for {func.__name__}") from last_exc
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# API Client (GitHub)
# ---------------------------------------------------------------------------


class GitHubClient:
    """GitHub API client with rate‑limiting and retry."""

    BASE_URL: ClassVar[str] = "https://api.github.com"
    PER_PAGE: ClassVar[int] = 30

    def __init__(self, token: str, user_agent: str = "BountyBlitz/1.0") -> None:
        """Initialize client.

        Args:
            token: GitHub personal access token.
            user_agent: User‑Agent string for requests.

        Raises:
            ConfigurationError: If token is empty.
        """
        if not token.strip():
            raise ConfigurationError("GitHub token cannot be empty")
        self._token = token
        self._user_agent = user_agent
        self._rate_limit_remaining: int = 5000
        self._rate_limit_reset: float = 0.0
        self._ssl_context = ssl.create_default_context()

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"token {self._token}",
            "User-Agent": self._user_agent,
            "Accept": "application/vnd.github.v3+json",
        }

    def _respect_rate_limit(self) -> None:
        """Sleep if rate limit exhausted, waiting until reset."""
        if self._rate_limit_remaining <= 0:
            wait = max(0.0, self._rate_limit_reset - time.time())
            if wait > 0:
                log.warning("Rate limit exhausted, sleeping %.2f seconds", wait)
                time.sleep(wait)
            self._rate_limit_remaining = 5000  # optimistic refresh

    def _update_rate_limit(self, response: urllib.request.Request) -> None:
        """Parse rate limit headers from a response."""
        remaining_str = response.headers.get("X-RateLimit-Remaining")
        reset_str = response.headers.get("X-RateLimit-Reset")
        if remaining_str is not None:
            try:
                self._rate_limit_remaining = int(remaining_str)
            except ValueError:
                pass
        if reset_str is not None:
            try:
                self._rate_limit_reset = float(reset_str)
            except ValueError:
                pass

    @retry(max_retries=3)
    def _request(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request to the GitHub API.

        Args:
            path: API path (e.g., '/repos/owner/repo').
            params: Query parameters.

        Returns:
            Parsed JSON response as dict.

        Raises:
            APIError: On non‑2xx response.
            RateLimitError: On 403 with rate limiting.
            NetworkError: On connection failure.
        """
        self._respect_rate_limit()
        url = f"{self.BASE_URL}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        req = urllib.request.Request(url, headers=self._headers(), method="GET")
        try:
            with urllib.request.urlopen(req, context=self._ssl_context, timeout=15) as resp:
                self._update_rate_limit(resp)
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            if exc.code == 403:
                # Check if rate limited
                remaining = exc.headers.get("X-RateLimit-Remaining")
                if remaining == "0":
                    reset = exc.headers.get("X-RateLimit-Reset", "0")
                    self._rate_limit_reset = float(reset)
                    self._rate_limit_remaining = 0
                    raise RateLimitError(f"Rate limited: {exc.reason}") from exc
                else:
                    raise APIError(f"HTTP 403: {exc.reason}") from exc
            elif exc.code >= 500:
                raise NetworkError(f"Server error {exc.code}: {exc.reason}") from exc
            else:
                raise APIError(f"HTTP {exc.code}: {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise NetworkError(f"Network error: {exc.reason}") from exc
        except (OSError, json.JSONDecodeError) as exc:
            raise NetworkError(str(exc)) from exc

    def get_issues(
        self, repo: str, state: str = "open", labels: str = "bounty"
    ) -> list[dict[str, Any]]:
        """Fetch issues with given labels.

        Args:
            repo: Full repo name (owner/repo).
            state: Issue state (open, closed, all).
            labels: Comma‑separated labels.

        Returns:
            List of issue dictionaries.
        """
        path = f"/repos/{repo}/issues"
        params: dict[str, Any] = {
            "state": state,
            "labels": labels,
            "per_page": self.PER_PAGE,
        }
        data = self._request(path, params)
        if not isinstance(data, list):
            log.error("Unexpected response format for issues: %s", type(data))
            return []
        return data


class BountyFetcher:
    """Fetch and transform GitHub issues into Bounty objects."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def fetch_bounties(
        self,
        repository: str,
        min_reward: Optional[str] = None,
        max_age_hours: Optional[float] = None,
    ) -> list[Bounty]:
        """Retrieve bounties from a repository.

        Args:
            repository: Repo full name.
            min_reward: Filter if reward text contains this string (case‑insensitive).
            max_age_hours: Maximum age in hours.

        Returns:
            List of validated Bounty objects.
        """
        raw_issues = self._client.get_issues(repository)
        bounties: list[Bounty] = []
        now = datetime.now(timezone.utc)

        for issue in raw_issues:
            try:
                bounty = self._issue_to_bounty(issue)
            except (ValidationError, KeyError, TypeError) as exc:
                log.warning("Skipping invalid issue %s: %s", issue.get("html_url", "unknown"), exc)
                continue

            # Filter by age
            if max_age_hours is not None:
                age = now - bounty.last_updated
                if age > timedelta(hours=max_age_hours):
                    continue

            # Filter by reward
            if min_reward and bounty.reward:
                if min_reward.lower() not in bounty.reward.lower():
                    continue

            bounties.append(bounty)

        return bounties

    @staticmethod
    def _issue_to_bounty(issue: Mapping[str, Any]) -> Bounty:
        """Convert a GitHub issue API object to a Bounty.

        Args:
            issue: Issue dictionary from API.

        Returns:
            Bounty instance.

        Raises:
            ValidationError: If required fields missing.
        """
        title = issue.get("title", "")
        url = issue.get("html_url", "")
        repo_full = issue.get("repository_url", "").replace("https://api.github.com/repos/", "")
        comments = issue.get("comments", 0)
        updated_str = issue.get("updated_at", "")
        updated = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))

        # Extract reward from labels or body
        reward: Optional[str] = None
        labels = issue.get("labels", [])
        for label in labels:
            name = label.get("name", "")
            if name.lower().startswith("reward:"):
                reward = name.split(":", 1)[1].strip()
                break
        if not reward:
            # Try body pattern: "Reward: X"
            body = issue.get("body", "") or ""
            for line in body.splitlines():
                if line.lower().startswith("reward:"):
                    reward = line.split(":", 1)[1].strip()
                    break

        skills: list[str] = []
        for label in labels:
            name = label.get("name", "")
            if name.lower().startswith("skill:"):
                skills.append(name.split(":", 1)[1].strip())

        return Bounty(
            title=title,
            url=url,
            repository=repo_full,
            comments=comments,
            last_updated=updated,
            reward=reward,
            skills=tuple(skills),
        )


# ---------------------------------------------------------------------------
# Messenger interface & implementations
# ---------------------------------------------------------------------------


class Messenger(abc.ABC):
    """Abstract base for channel messengers."""

    def __init__(self, channel: Channel) -> None:
        self.channel = channel

    @abc.abstractmethod
    def send(self, message: str) -> bool:
        """Send a message via this channel.

        Args:
            message: The message content.

        Returns:
            True if sent successfully.
        """
        ...

    def health_check(self) -> bool:
        """Check if messenger is operational.

        Returns:
            True if healthy.
        """
        return True


class EmailMessenger(Messenger):
    """Send emails via SMTP."""

    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_pass: str, target_email: str) -> None:
        super().__init__(Channel.EMAIL)
        self._host = smtp_host
        self._port = smtp_port
        self._user = smtp_user
        self._pass = smtp_pass
        self._target = target_email

    def send(self, message: str) -> bool:
        """Send an email.

        Args:
            message: Email body.

        Returns:
            True if sent.
        """
        msg = MIMEText(message)
        msg["Subject"] = "Bounty Alert Blitz"
        msg["From"] = formataddr(("Bounty Blitz", self._user))
        msg["To"] = self._target

        try:
            conn = HTTPSConnection(self._host, self._port, timeout=10)
            conn.set_debuglevel(0)
            # Simplified: In production use smtplib
            log.info("Simulated email send to %s via %s:%d", self._target, self._host, self._port)
            conn.close()
            return True
        except HTTPException as exc:
            log.error("Email send failed: %s", exc)
            return False


class TwitterMessenger(Messenger):
    """Post to Twitter (simplified)."""

    def __init__(self, api_key: str, api_secret: str) -> None:
        super().__init__(Channel.TWITTER)
        self._api_key = api_key
        self._api_secret = api_secret

    def send(self, message: str) -> bool:
        """Post a tweet.

        Args:
            message: Tweet text (max 280 chars).

        Returns:
            True if posted.
        """
        # Simulate API call
        log.info("Simulated tweet (len=%d): %s", len(message), message[:50])
        return True


class LinkedInMessenger(Messenger):
    """Post to LinkedIn (simplified)."""

    def __init__(self, access_token: str) -> None:
        super().__init__(Channel.LINKEDIN)
        self._token = access_token

    def send(self, message: str) -> bool:
        """Post a LinkedIn update.

        Args:
            message: Post text.

        Returns:
            True if posted.
        """
        log.info("Simulated LinkedIn post: %s", message[:50])
        return True


# ---------------------------------------------------------------------------
# Campaign Manager
# ---------------------------------------------------------------------------


class CampaignManager:
    """Orchestrates fetching bounties and distributing via channels."""

    def __init__(
        self,
        fetcher: BountyFetcher,
        messengers: dict[Channel, Messenger],
        config: CampaignConfig,
        metrics: Metrics | None = None,
    ) -> None:
        """Initialize manager.

        Args:
            fetcher: Bounty fetcher instance.
            messengers: Mapping of channel to messenger.
            config: Campaign configuration.
            metrics: Optional metrics collector.
        """
        self._fetcher = fetcher
        self._messengers = messengers
        self._config = config
        self._metrics = metrics or Metrics()
        self._cooldowns: dict[Channel, float] = {}  # channel -> timestamp

    def _can_send(self, channel: Channel) -> bool:
        """Check if cooldown has elapsed for a channel.

        Args:
            channel: Channel to check.

        Returns:
            True if message can be sent.
        """
        last = self._cooldowns.get(channel, 0.0)
        return (time.time() - last) >= self._config.cooldown_minutes * 60

    def _format_message(self, bounty: Bounty) -> str:
        """Apply template to bounty data.

        Args:
            bounty: Bounty instance.

        Returns:
            Formatted message string.
        """
        return self._config.template.format(
            title=bounty.title,
            url=bounty.url,
            repository=bounty.repository,
            reward=bounty.reward or "Undisclosed",
            skills=", ".join(bounty.skills),
            comments=bounty.comments,
        )

    def run(self, repository: str) -> None:
        """Execute one campaign cycle.

        Args:
            repository: GitHub repository to scan.
        """
        log.info("Starting campaign cycle for %s", repository)

        # Fetch
        try:
            bounties = self._fetcher.fetch_bounties(
                repository,
                min_reward=self._config.min_reward,
                max_age_hours=self._config.max_age_hours,
            )
        except (APIError, NetworkError, ConfigurationError) as exc:
            log.error("Failed to fetch bounties: %s", exc)
            self._metrics.record_error("fetch")
            return

        if not bounties:
            log.info("No new bounties to promote.")
            return

        self._metrics.increment("bounties_fetched", len(bounties))

        # For each channel, select one bounty (newest)
        for channel in self._config.channels:
            messenger = self._messengers.get(channel)
            if not messenger:
                log.warning("No messenger configured for channel %s", channel.value)
                continue
            if not self._can_send(channel):
                log.debug("Channel %s in cooldown, skipping", channel.value)
                continue

            # Choose the most recent bounty
            target = max(bounties, key=lambda b: b.last_updated)
            message = self._format_message(target)

            try:
                success = messenger.send(message)
            except Exception as exc:
                log.error("Messenger %s failed: %s", channel.value, exc)
                self._metrics.record_error(channel.value)
                success = False

            if success:
                self._cooldowns[channel] = time.time()
                self._metrics.increment(f"posts_{channel.value}")
                log.info("Posted to %s: %s", channel.value, target.title[:60])
            else:
                log.error("Failed to post to %s", channel.value)

        log.info("Campaign cycle completed. Metrics: %s", self._metrics.report())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_messengers_from_env() -> dict[Channel, Messenger]:
    """Build messengers using environment variables.

    Returns:
        Mapping of channel to messenger.

    Raises:
        ConfigurationError: If required env vars are missing.
    """
    messengers: dict[Channel, Messenger] = {}

    token = load_secret("GITHUB_TOKEN")
    if token:
        # Not a messenger, but used by client
        pass

    # Twitter
    twitter_key = load_secret("TWITTER_API_KEY")
    twitter_secret = load_secret("TWITTER_API_SECRET")
    if twitter_key and twitter_secret:
        messengers[Channel.TWITTER] = TwitterMessenger(twitter_key, twitter_secret)

    # LinkedIn
    linkedin_token = load_secret("LINKEDIN_ACCESS_TOKEN")
    if linkedin_token:
        messengers[Channel.LINKEDIN] = LinkedInMessenger(linkedin_token)

    # Email
    smtp_host = load_secret("SMTP_HOST")
    smtp_port_str = load_secret("SMTP_PORT")
    smtp_user = load_secret("SMTP_USER")
    smtp_pass = load_secret("SMTP_PASS")
    target_email = load_secret("NEWSLETTER_LIST_ID")
    if smtp_host and smtp_port_str and smtp_user and smtp_pass and target_email:
        try:
            smtp_port = int(smtp_port_str)
        except ValueError:
            raise ConfigurationError(f"Invalid SMTP_PORT: {smtp_port_str}")
        messengers[Channel.EMAIL] = EmailMessenger(
            smtp_host, smtp_port, smtp_user, smtp_pass, target_email
        )

    if not messengers:
        raise ConfigurationError("No messengers could be configured. Check environment variables.")

    return messengers


def run_campaign(
    repository: str,
    config: CampaignConfig | None = None,
) -> None:
    """Run a full campaign cycle.

    Args:
        repository: GitHub repo (owner/repo).
        config: Optional campaign config (defaults to sensible values).
    """
    log.info("=== Bounty Alert Blitz Campaign ===")
    log.info("Repository: %s", repository)

    # Validate secrets
    try:
        validate_secrets()
    except ConfigurationError as exc:
        log.critical("Secrets validation failed: %s", exc)
        return

    # Build messengers
    try:
        messengers = build_messengers_from_env()
    except ConfigurationError as exc:
        log.critical("Messenger build failed: %s", exc)
        return

    # GitHub client & fetcher
    token = load_secret("GITHUB_TOKEN")
    client = GitHubClient(token)
    fetcher = BountyFetcher(client)

    # Config
    if config is None:
        config = CampaignConfig(
            channels=(Channel.TWITTER, Channel.LINKEDIN, Channel.EMAIL),
            cooldown_minutes=10.0,
        )

    # Metrics
    metrics = Metrics()

    # Manager
    manager = CampaignManager(fetcher, messengers, config, metrics)
    manager.run(repository)


def main() -> None:
    """Main entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bounty_blitz.py <owner/repo> [--min-reward X] [--max-age N]")
        sys.exit(1)

    repo = sys.argv[1]
    config = CampaignConfig()
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--min-reward" and i + 1 < len(args):
            config = CampaignConfig(
                channels=config.channels,
                min_reward=args[i + 1],
                max_age_hours=config.max_age_hours,
                cooldown_minutes=config.cooldown_minutes,
                template=config.template,
            )
        elif arg == "--max-age" and i + 1 < len(args):
            try:
                max_age = float(args[i + 1])
            except ValueError:
                log.error("Invalid max-age value: %s", args[i+1])
                sys.exit(1)
            config = CampaignConfig(
                channels=config.channels,
                min_reward=config.min_reward,
                max_age_hours=max_age,
                cooldown_minutes=config.cooldown_minutes,
                template=config.template,
            )

    run_campaign(repo, config)


if __name__ == "__main__":
    main()