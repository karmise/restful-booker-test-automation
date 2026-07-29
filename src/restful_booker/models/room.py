"""Seeded room models used by UI scenarios."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Room:
    """Stable public information for a seeded room."""

    room_id: int
    name: str
    nightly_rate: int
    features: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.room_id <= 0:
            raise ValueError("room_id must be greater than zero")
        if self.nightly_rate <= 0:
            raise ValueError("nightly_rate must be greater than zero")
