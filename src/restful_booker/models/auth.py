"""Administration authentication models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Credentials:
    """Credentials entered through the administrator login form."""

    username: str
    password: str
