"""Typed request and response data transfer objects."""

from restful_booker.api.dto.auth import AuthRequest, TokenResponse
from restful_booker.api.dto.booking import (
    ApiBookingDates,
    BookingCollection,
    BookingRequest,
    BookingResponse,
)
from restful_booker.api.dto.message import (
    MessageCollection,
    MessageRequest,
    MessageSummary,
)
from restful_booker.api.dto.room import RoomCollection, RoomRequest, RoomResponse

__all__ = [
    "ApiBookingDates",
    "AuthRequest",
    "BookingCollection",
    "BookingRequest",
    "BookingResponse",
    "MessageCollection",
    "MessageRequest",
    "MessageSummary",
    "RoomCollection",
    "RoomRequest",
    "RoomResponse",
    "TokenResponse",
]
