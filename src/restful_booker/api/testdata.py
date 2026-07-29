"""Unique API payload factories for isolated resource lifecycles."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
from uuid import uuid4

from restful_booker.api.dto import (
    ApiBookingDates,
    AuthRequest,
    BookingRequest,
    MessageRequest,
    RoomRequest,
)


class ApiTestDataFactory:
    """Create valid and deliberately invalid API request DTOs."""

    def auth_request(self, *, username: str, password: str) -> AuthRequest:
        """Build typed authentication input."""

        return AuthRequest(username=username, password=password)

    def room_request(self) -> RoomRequest:
        """Build a uniquely named room owned by the current test."""

        token = _short_token()
        return RoomRequest(
            room_name=f"api-{token}",
            room_type="Double",
            accessible=True,
            image="/images/room2.jpg",
            description=f"Automated API lifecycle room {token}.",
            features=("TV", "WiFi", "Safe"),
            room_price=175,
        )

    def booking_request(
        self,
        *,
        room_id: int,
        starts_in_days: int = 60,
        nights: int = 2,
    ) -> BookingRequest:
        """Build a valid booking with a unique guest identity."""

        token = _short_token()
        check_in = date.today() + timedelta(days=starts_in_days)
        return BookingRequest(
            room_id=room_id,
            first_name="Api",
            last_name=f"Guest{token}",
            deposit_paid=False,
            dates=ApiBookingDates(
                check_in=check_in,
                check_out=check_in + timedelta(days=nights),
            ),
            email=f"api.{token}@example.com",
            phone="01234567890",
        )

    def booking_with_invalid_guest(self, *, room_id: int) -> BookingRequest:
        """Build a booking that isolates guest-field validation."""

        valid = self.booking_request(room_id=room_id)
        return replace(
            valid,
            first_name="",
            email="invalid-email",
            phone="123",
        )

    def booking_with_reversed_dates(self, *, room_id: int) -> BookingRequest:
        """Build a booking whose checkout precedes check-in."""

        valid = self.booking_request(room_id=room_id)
        return replace(
            valid,
            dates=ApiBookingDates(
                check_in=valid.dates.check_in,
                check_out=valid.dates.check_in - timedelta(days=1),
            ),
        )

    def message_request(self) -> MessageRequest:
        """Build a uniquely identifiable valid contact message."""

        token = _short_token()
        return MessageRequest(
            name=f"API User {token}",
            email=f"api.{token}@example.com",
            phone="01234567890",
            subject=f"API lifecycle {token}",
            description=(
                f"This message verifies the complete API resource lifecycle. Reference: {token}."
            ),
        )

    def message_with_invalid_email(self) -> MessageRequest:
        """Build a complete message that isolates email validation."""

        return replace(self.message_request(), email="invalid-email")


def _short_token() -> str:
    return uuid4().hex[:8]
