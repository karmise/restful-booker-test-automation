"""Environment-backed framework settings."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated settings shared by fixtures and page objects."""

    base_url: str
    admin_username: str
    admin_password: str = field(repr=False)
    action_timeout_ms: int
    navigation_timeout_ms: int
    api_timeout_s: int
    api_connect_timeout_s: int = 5

    @property
    def api_timeout(self) -> tuple[int, int]:
        """Requests connect/read timeouts; neither is a total request deadline."""

        return self.api_connect_timeout_s, self.api_timeout_s

    @classmethod
    def from_env(cls) -> Settings:
        """Build settings from environment variables with sandbox defaults."""

        return cls(
            base_url=_base_url(),
            admin_username=os.getenv("RBP_ADMIN_USERNAME", "admin"),
            admin_password=os.getenv("RBP_ADMIN_PASSWORD", "password"),
            action_timeout_ms=_positive_int("RBP_ACTION_TIMEOUT_MS", default=10_000),
            navigation_timeout_ms=_positive_int(
                "RBP_NAVIGATION_TIMEOUT_MS",
                default=30_000,
            ),
            api_timeout_s=_positive_int("RBP_API_TIMEOUT_S", default=15),
            api_connect_timeout_s=_positive_int("RBP_API_CONNECT_TIMEOUT_S", default=5),
        )


def _positive_int(name: str, *, default: int) -> int:
    raw_value = os.getenv(name)
    try:
        value = default if raw_value is None else int(raw_value)
    except ValueError:
        raise ValueError(f"{name} must be a positive integer") from None
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def _base_url() -> str:
    value = os.getenv("RBP_BASE_URL", "https://automationintesting.online").strip().rstrip("/")
    try:
        parsed = urlsplit(value)
        valid = (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and not parsed.query
            and not parsed.fragment
            and not any(character.isspace() for character in value)
        )
        _ = parsed.port  # Validate malformed and out-of-range ports as well.
    except ValueError:
        valid = False
    if not valid:
        raise ValueError(
            "RBP_BASE_URL must be an HTTP(S) URL without credentials, query or fragment"
        )
    return value
