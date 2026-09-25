"""Administration authentication models."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Credentials:
    """Credentials entered through the administrator login form."""

    username: str
    password: str = field(repr=False)
