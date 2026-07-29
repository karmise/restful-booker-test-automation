"""Typed UI input models."""

from restful_booker.models.auth import Credentials
from restful_booker.models.booking import BookingRequest, GuestDetails, StayPeriod
from restful_booker.models.contact import ContactMessage
from restful_booker.models.room import Room

__all__ = [
    "BookingRequest",
    "ContactMessage",
    "Credentials",
    "GuestDetails",
    "Room",
    "StayPeriod",
]
