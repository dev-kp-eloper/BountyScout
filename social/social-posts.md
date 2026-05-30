"""
Social Media Campaign Generator for Bounty Alert Blitz 2026.

This module provides production-ready structures and functions to generate,
validate, and log social media posts for open source bounty campaigns.

Usage:
    from social_posts import Campaign, TwitterPost, LinkedInPost, RedditPost
    campaign = Campaign.load_default()
    campaign.generate_all()
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("campaign_generation.log", mode="a"),
    ],
)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Data Validation
# ------------------------------------------------------------------------------
class ValidationError(Exception):
    """Custom exception for data validation failures."""


def validate_url(url: str) -> bool:
    """Validate a GitHub issue URL format.

    Args:
        url: The URL to validate.

    Returns:
        True if the URL matches the expected pattern.

    Raises:
        ValidationError: If url is empty or malformed.
    """
    if not url or not url.startswith("https://github.com/"):
        raise ValidationError(f"Invalid GitHub URL: {url!r}")
    # Further checks could be added (e.g., regex)
    return True


def validate_date(date_str: str) -> bool:
    """Validate a date string in YYYY-MM-DD format.

    Args:
        date_str: The date string.

    Returns:
        True if valid.

    Raises:
        ValidationError: If format is wrong.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValidationError(f"Invalid date format: {date_str!r}") from exc
    return True


# ------------------------------------------------------------------------------
# Post Data Classes
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Bounty:
    """Represents a single open-source bounty entry."""

    title: str
    repository: str
    issue_number: int
    url: str
    description: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate fields after initialization."""
        try:
            validate_url(self.url)
        except ValidationError as exc:
            logger.error("Invalid bounty URL: %s", exc)
            raise
        if not self.title or not self.repository:
            raise ValidationError("Bounty title and repository are required.")
        logger.debug("Bounty created: %s", self.url)


@dataclass
class Post:
    """Base class for a social media post.

    Attributes:
        platform: The social media platform (twitter, linkedin, reddit).
        day: Campaign day number (1-based).
        text: Main body text.
        schedule_time: Optional time string for scheduling.
        hashtags: List of tags to include.
        urls: Related bounty URLs.
    """

    platform: str
    day: int
    text: str
    schedule_time: Optional[str] = None
    hashtags: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate post fields."""
        if self.day < 1 or self.day > 14:
            raise ValidationError(f"Campaign day out of range: {self.day}")
        if not self.text:
            raise ValidationError("Post text cannot be empty.")
        for url in self.urls:
            validate_url(url)
        logger.info("Post validated for %s, day %d", self.platform, self.day)


@dataclass
class TwitterPost(Post):
    """Twitter-specific post with character limit enforcement."""

    MAX_LENGTH: int = 280

    def __post_init__(self) -> None:
        """Enforce max character limit."""
        super().__post_init__()
        if len(self.text) > self.MAX_LENGTH:
            # Truncate gracefully
            self.text = self.text[: self.MAX_LENGTH - 3] + "..."
            logger.warning("Twitter post truncated to %d characters", self.MAX_LENGTH)


@dataclass
class LinkedInPost(Post):
    """LinkedIn post with headline support."""

    headline: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.headline:
            logger.warning("LinkedIn post without headline on day %d", self.day)


@dataclass
class RedditPost(Post):
    """Reddit post with subreddit and title."""

    subreddit: str = ""
    title: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.subreddit or not self.title:
            raise ValidationError("Reddit post requires subreddit and title.")


# ------------------------------------------------------------------------------
# Campaign Class
# ------------------------------------------------------------------------------
class Campaign:
    """Manages the entire bounty alert campaign.

    Args:
        name: Campaign display name.
        scan_date: UTC timestamp of the scan.
        bounties: List of Bounty objects.
        posts: Collection of scheduled posts.
    """

    def __init__(
        self,
        name: str,
        scan_date: str,
        bounties: List[Bounty],
        posts: Optional[List[Post]] = None,
    ) -> None:
        self.name = name
        self.scan_date = scan_date
        self.bounties = bounties
        self.posts = posts or []
        self._validate()

    def _validate(self) -> None:
        """Validate campaign metadata."""
        validate_date(self.scan_date)
        if not self.bounties:
            raise ValidationError("Campaign must contain at least one bounty.")
        logger.info("Campaign '%s' initialized with %d bounties", self.name, len(self.bounties))

    def add_post(self, post: Post) -> None:
        """Add a post to the campaign schedule.

        Args:
            post: A validated Post object.
        """
        self.posts.append(post)
        logger.debug("Post added for %s, day %d", post.platform, post.day)

    def generate_text(self, post: Post) -> str:
        """Generate the full formatted text for a post.

        Args:
            post: The Post object to render.

        Returns:
            Formatted string suitable for publishing.
        """
        parts = [post.text]
        if post.hashtags:
            parts.append("\n" + " ".join(f"#{tag}" for tag in post.hashtags))
        if post.urls:
            parts.append("\n" + "\n".join(post.urls))
        if isinstance(post, LinkedInPost) and post.headline:
            parts.insert(0, f"**{post.headline}**\n")
        if isinstance(post, RedditPost):
            parts.insert(0, f"**r/{post.subreddit}** – {post.title}\n")
        return "\n\n".join(parts)

    def generate_all(self) -> List[Dict[str, Any]]:
        """Generate all posts and return structured output.

        Returns:
            A list of dictionaries with platform, day, text, and metadata.
        """
        output = []
        for post in self.posts:
            full_text = self.generate_text(post)
            entry = {
                "platform": post.platform,
                "day": post.day,
                "text": full_text,
                "schedule_time": post.schedule_time,
                "urls": post.urls,
            }
            output.append(entry)
            logger.info("Generated %s post for day %d", post.platform, post.day)
        return output

    @classmethod
    def load_default(cls) -> "Campaign":
        """Factory method that builds the default campaign from the original spec.

        Returns:
            Fully populated Campaign instance.
        """
        logger.info("Loading default campaign from specification")
        bounties = [
            Bounty(
                title="Campaign Builder: delete block sends GET instead of POST",
                repository="mautic/mautic",
                issue_number=16185,
                url="https://github.com/mautic/mautic/issues/16185",
            ),
            Bounty(
                title="Bounty Claim System",
                repository="Scottcjn/rustchain-bounties",
                issue_number=12579,
                url="https://github.com/Scottcjn/rustchain-bounties/issues/12579",
            ),
            Bounty(
                title="Marketing: legal stack — /cookies, /dpa, /sla, /security/responsible-disclosure",
                repository="0xdevcollins/useroutr",
                issue_number=142,
                url="https://github.com/0xdevcollins/useroutr/issues/142",
            ),
            Bounty(
                title="moment-1.7.2.min.js: 5 vulnerabilities (highest severity 8.7)",
                repository="GHCbflam1/RailsGoat",
                issue_number=10,
                url="https://github.com/GHCbflam1/RailsGoat/issues/10",
            ),
            Bounty(
                title="Build public test-mode Publish Settings for database-backed integration keys",
                repository="mergeos-bounties/mergeos",
                issue_number=141,
                url="https://github.com/mergeos-bounties/mergeos/issues/141",
            ),
        ]

        campaign = cls(
            name="🚀 Bounty Alert Blitz: 5 New Open Source Gigs",
            scan_date="2026-05-29",
            bounties=bounties,
        )

        # --- Day 1: Awareness ---
        twitter_day1_text = (
            "5 fresh open-source bounties are live and waiting for you! 🎯\n"
            "From Rails security patches to Rust blockchain fixes – something for every stack.\n\n"
            "🔹 Mautic: `data-method` bug\n🔹 Rustchain: bounty claim system\n"
            "🔹 useroutr: legal stack docs\n🔹 RailsGoat: moment.js vulnerability (CVSS 8.7!)\n"
            "🔹 MergeOS: test-mode publish settings\n\n"
            "Click each to review and claim 👇"
        )
        campaign.add_post(
            TwitterPost(
                platform="twitter",
                day=1,
                text=twitter_day1_text,
                hashtags=["OpenSource", "BountyHunter", "Rust", "GoLang", "RubyOnRails", "BugBounty"],
                urls=[b.url for b in bounties],
            )
        )

        linkedin_day1 = LinkedInPost(
            platform="linkedin",
            day=1,
            headline="🚨 5 New Open Source Bounties – Apply Your Skills in Rust, Go, or Rails",
            text="Great opportunity for developers to contribute to real-world projects and earn rewards. "
                 "The latest batch of bounties covers:\n\n"
                 + "\n".join(f"🔹 **{b.title}** – {b.repository}" for b in bounties)
                 + "\n\nEach issue is ready for your contribution. Review the requirements, submit a PR, and make an impact.",
            hashtags=["OpenSource", "Bounty", "RustLang", "GoLang", "RubyOnRails", "DeveloperCommunity", "BugBounty", "Contributor"],
            urls=[b.url for b in bounties],
        )
        campaign.add_post(linkedin_day1)

        # Day 3 – RailsGoat deep dive thread (simplified)
        railsgoat = bounties[3]
        twitter_thread_text = (
            f"🧵 1/4\nCritical moment.js vulnerability in {railsgoat.repository} – CVSS 8.7!\n"
            "This is your chance to fix a real security issue and earn a bounty.\n\n"
            "2/4 The bug affects `moment-1.7.2.min.js` – an old, unmaintained version.\n"
            "Replace it? Patch it? Upgrade to a modern library?\n\n"
            "3/4 Check the full issue here 👇\n"
            f"{railsgoat.url}\n\n"
            "4/4 Even if you’re new to security research, this is a great beginner-friendly bounty.\n"
            "Don’t wait – submit a PR before it’s taken!"
        )
        campaign.add_post(
            TwitterPost(
                platform="twitter",
                day=3,
                text=twitter_thread_text,
                hashtags=["Rails", "InfoSec", "BountyHunter", "OpenSource"],
                urls=[railsgoat.url],
            )
        )

        # Day 5 – MergeOS focused
        mergeos = bounties[4]
        linkedin_day5 = LinkedInPost(
            platform="linkedin",
            day=5,
            headline="Build Integration Keys for a Growing APIs Platform – MergeOS Bounty",
            text=f"MergeOS is offering $5,000 MRG (their token) for building a public test-mode publish settings system. "
                 "This is a backend-heavy task requiring Go or database experience.\n\n"
                 f"The issue already has 3 comments, so act fast.\n{mergeos.url}\n\n"
                 "**Bonus:** If you’re interested in API integrations, this can lead to more paid work.",
            hashtags=["GoLang", "API", "Integration", "Bounty", "OpenSource"],
            urls=[mergeos.url],
        )
        campaign.add_post(linkedin_day5)

        # Reddit posts
        rust_bounties = [bounties[0], bounties[1]]  # Mautic and Rustchain
        campaign.add_post(
            RedditPost(
                platform="reddit",
                day=1,
                subreddit="rust",
                title="🦀 2 Rust-related bounties open right now (one from Rustchain)",
                text="Fellow Rustaceans, there’s a fresh bounty on **Rustchain bounties** (link below) "
                     "that builds a bounty claim system in Rust. Great way to contribute and earn rewards.\n\n"
                     + "\n".join(f"- [{b.title}]({b.url})" for b in rust_bounties),
                urls=[b.url for b in rust_bounties],
                hashtags=["Rust", "Bounty", "OpenSource"],
            )
        )

        campaign.add_post(
            RedditPost(
                platform="reddit",
                day=1,
                subreddit="golang",
                title="🔵 Want to work with Go? MergeOS is paying $5,000 for a test-mode publish settings feature",
                text=f"Hey Gophers! The MergeOS team is offering 5,000 MRG for building a database-backed test-mode "
                     f"environment for integration keys.\n\n{mergeos.url}\n\n"
                     "If you’ve experience with Go, PostgreSQL, and API design, this is a perfect weekend project.",
                urls=[mergeos.url],
                hashtags=["GoLang", "Bounty", "OpenSource", "Backend"],
            )
        )

        campaign.add_post(
            RedditPost(
                platform="reddit",
                day=1,
                subreddit="rails",
                title="💎 3 Rails-related bounties: security, legal docs, and a campaign builder bug",
                text="rails devs – we have three fresh bounties that need your Ruby on Rails expertise:\n\n"
                     + "\n".join(f"{i+1}. **{b.title}** – {b.url}" for i, b in enumerate([bounties[2], bounties[3], bounties[0]]))
                     + "\n\nAll are open to new contributors. Let’s help the open source community!",
                urls=[bounties[2].url, bounties[3].url, bounties[0].url],
                hashtags=["Rails", "Ruby", "Bounty", "BugBounty", "OpenSource"],
            )
        )

        logger.info("Default campaign loaded with %d posts", len(campaign.posts))
        return campaign


# ------------------------------------------------------------------------------
# Main Execution (if run as script)
# ------------------------------------------------------------------------------
def main() -> None:
    """Build and print the default campaign posts."""
    try:
        campaign = Campaign.load_default()
        posts = campaign.generate_all()
        for entry in posts:
            print(f"\n{'='*60}")
            print(f"[{entry['platform'].upper()}] Day {entry['day']}")
            print(entry['text'])
            print(f"{'='*60}\n")
        logger.info("Campaign generation completed successfully.")
    except ValidationError as e:
        logger.critical("Campaign validation failed: %s", e)
        raise SystemExit(1) from e
    except Exception:
        logger.exception("Unexpected error during campaign generation.")
        raise


if __name__ == "__main__":
    main()