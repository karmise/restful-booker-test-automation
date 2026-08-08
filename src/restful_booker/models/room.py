"""Room models used by UI scenarios."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Room:
    """Public room information required by UI assertions."""

    room_id: int
    name: str
    room_type: str
    nightly_rate: int
    features: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.room_id <= 0:
            raise ValueError("room_id must be greater than zero")
        if self.nightly_rate <= 0:
            raise ValueError("nightly_rate must be greater than zero")
