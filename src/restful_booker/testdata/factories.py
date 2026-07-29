"""Deterministic-shape test data with unique identities."""

from __future__ import annotations

from datetime import date, timedelta
from uuid import uuid4

from restful_booker.models import (
    BookingRequest,
    ContactMessage,
    GuestDetails,
    StayPeriod,
)


class TestDataFactory:
    """Create independent test inputs without coupling tests to Faker."""

    def contact_message(self) -> ContactMessage:
        token = _short_token()
        return ContactMessage(
            name=f"Portfolio User {token}",
            email=f"portfolio.{token}@example.com",
            phone="01234567890",
            subject=f"Booking question {token}",
            message=(
                "Please confirm whether breakfast is included with the room "
                f"reservation. Reference: {token}."
            ),
        )

    def booking_request(self, *, starts_in_days: int = 30, nights: int = 2) -> BookingRequest:
        if starts_in_days < 1:
            raise ValueError("starts_in_days must be at least one")
        if nights < 1:
            raise ValueError("nights must be at least one")

        token = _short_token()
        check_in = date.today() + timedelta(days=starts_in_days)
        stay = StayPeriod(
            check_in=check_in,
            check_out=check_in + timedelta(days=nights),
        )
        guest = GuestDetails(
            first_name="Portfolio",
            last_name=f"Guest{token}",
            email=f"guest.{token}@example.com",
            phone="01234567890",
        )
        return BookingRequest(stay=stay, guest=guest)


def _short_token() -> str:
    return uuid4().hex[:8]
