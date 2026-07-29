"""Booking API contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from restful_booker.api.dto._parsing import (
    as_array,
    as_object,
    required_bool,
    required_int,
    required_str,
)
from restful_booker.api.types import JsonValue


@dataclass(frozen=True, slots=True)
class ApiBookingDates:
    """Check-in and check-out dates sent through the API."""

    check_in: date
    check_out: date

    def to_payload(self) -> dict[str, JsonValue]:
        """Serialize dates using the service field names."""

        return {
            "checkin": self.check_in.isoformat(),
            "checkout": self.check_out.isoformat(),
        }


@dataclass(frozen=True, slots=True)
class BookingRequest:
    """Booking creation payload."""

    room_id: int
    first_name: str
    last_name: str
    deposit_paid: bool
    dates: ApiBookingDates
    email: str
    phone: str

    def to_payload(self) -> dict[str, JsonValue]:
        """Serialize booking data using the external API field names."""

        return {
            "roomid": self.room_id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "depositpaid": self.deposit_paid,
            "bookingdates": self.dates.to_payload(),
            "email": self.email,
            "phone": self.phone,
        }


@dataclass(frozen=True, slots=True)
class BookingResponse:
    """Booking returned from an authenticated room booking search."""

    booking_id: int
    room_id: int
    first_name: str
    last_name: str
    deposit_paid: bool
    dates: ApiBookingDates

    @classmethod
    def from_payload(cls, payload: object) -> BookingResponse:
        """Parse a booking response."""

        data = as_object(payload, context="Booking")
        booking_dates = as_object(data.get("bookingdates"), context="'bookingdates'")
        return cls(
            booking_id=required_int(data, "bookingid"),
            room_id=required_int(data, "roomid"),
            first_name=required_str(data, "firstname"),
            last_name=required_str(data, "lastname"),
            deposit_paid=required_bool(data, "depositpaid"),
            dates=ApiBookingDates(
                check_in=date.fromisoformat(required_str(booking_dates, "checkin")),
                check_out=date.fromisoformat(required_str(booking_dates, "checkout")),
            ),
        )


@dataclass(frozen=True, slots=True)
class BookingCollection:
    """Collection of bookings associated with a room."""

    bookings: tuple[BookingResponse, ...]

    @classmethod
    def from_payload(cls, payload: object) -> BookingCollection:
        """Parse a booking collection response."""

        data = as_object(payload, context="Booking collection response")
        bookings = as_array(data.get("bookings"), context="'bookings'")
        return cls(bookings=tuple(BookingResponse.from_payload(booking) for booking in bookings))

    def find_by_guest(self, *, first_name: str, last_name: str) -> BookingResponse:
        """Find a booking created for a unique test guest."""

        matches = [
            booking
            for booking in self.bookings
            if booking.first_name == first_name and booking.last_name == last_name
        ]
        if len(matches) != 1:
            raise LookupError(
                f"Expected one booking for '{first_name} {last_name}', found {len(matches)}"
            )
        return matches[0]
