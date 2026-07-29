"""Service-focused HTTP clients."""

from restful_booker.api.clients.auth_client import AuthClient
from restful_booker.api.clients.booking_client import BookingClient
from restful_booker.api.clients.branding_client import BrandingClient
from restful_booker.api.clients.message_client import MessageClient
from restful_booker.api.clients.report_client import ReportClient
from restful_booker.api.clients.room_client import RoomClient

__all__ = [
    "AuthClient",
    "BookingClient",
    "BrandingClient",
    "MessageClient",
    "ReportClient",
    "RoomClient",
]
