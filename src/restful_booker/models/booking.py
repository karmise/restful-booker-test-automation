"""Reservation form models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class StayPeriod:
    """Check-in and check-out dates selected in the UI."""

    check_in: date
    check_out: date

    def __post_init__(self) -> None:
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be later than check_in")

    @property
    def nights(self) -> int:
        """Number of nights represented by the period."""

        return (self.check_out - self.check_in).days


@dataclass(frozen=True, slots=True)
class GuestDetails:
    """Guest data entered into the reservation form."""

    first_name: str
    last_name: str
    email: str
    phone: str


@dataclass(frozen=True, slots=True)
class BookingRequest:
    """Complete UI input required to submit a reservation."""

    stay: StayPeriod
    guest: GuestDetails
