"""Environment-backed framework settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated settings shared by fixtures and page objects."""

    base_url: str
    admin_username: str
    admin_password: str
    action_timeout_ms: int
    navigation_timeout_ms: int

    @classmethod
    def from_env(cls) -> Settings:
        """Build settings from environment variables with sandbox defaults."""

        return cls(
            base_url=os.getenv(
                "RBP_BASE_URL",
                "https://automationintesting.online",
            ).rstrip("/"),
            admin_username=os.getenv("RBP_ADMIN_USERNAME", "admin"),
            admin_password=os.getenv("RBP_ADMIN_PASSWORD", "password"),
            action_timeout_ms=_positive_int("RBP_ACTION_TIMEOUT_MS", default=10_000),
            navigation_timeout_ms=_positive_int(
                "RBP_NAVIGATION_TIMEOUT_MS",
                default=30_000,
            ),
        )


def _positive_int(name: str, *, default: int) -> int:
    raw_value = os.getenv(name)
    value = default if raw_value is None else int(raw_value)
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value
