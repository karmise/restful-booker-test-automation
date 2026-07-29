"""Booking service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.api.dto import BookingRequest


class BookingClient(BaseApiClient):
    """Public creation and authenticated booking administration operations."""

    def get_bookings_for_room(self, room_id: int) -> Response:
        """Return bookings associated with a room."""

        return self._request("GET", "/booking", params={"roomid": room_id})

    def get_booking(self, booking_id: int) -> Response:
        """Return a booking by identifier."""

        return self._request("GET", f"/booking/{booking_id}")

    def create_booking(self, booking: BookingRequest) -> Response:
        """Create a guest booking."""

        return self._request(
            "POST",
            "/booking",
            payload=booking.to_payload(),
        )

    def delete_booking(self, booking_id: int) -> Response:
        """Delete a booking using the current session."""

        return self._request("DELETE", f"/booking/{booking_id}")
