"""API fixture imports scoped to the API test suite."""

from tests.api.fixtures.assertions import (
    api_assertions,
    auth_assertions,
    booking_assertions,
    branding_assertions,
    message_assertions,
    report_assertions,
    room_assertions,
    schema_registry,
)
from tests.api.fixtures.clients import (
    admin_booking_client,
    admin_message_client,
    admin_room_client,
    auth_client,
    authenticated_session,
    booking_client,
    branding_client,
    message_client,
    public_session,
    report_client,
    room_client,
)
from tests.api.fixtures.configuration import settings
from tests.api.fixtures.data import (
    api_test_data_factory,
    invalid_api_credentials,
    invalid_message_request,
    room_request,
    valid_api_credentials,
)
from tests.api.fixtures.resources import (
    created_booking,
    created_message,
    created_room,
)

__all__ = [
    "admin_booking_client",
    "admin_message_client",
    "admin_room_client",
    "api_assertions",
    "api_test_data_factory",
    "auth_assertions",
    "auth_client",
    "authenticated_session",
    "booking_assertions",
    "booking_client",
    "branding_assertions",
    "branding_client",
    "created_booking",
    "created_message",
    "created_room",
    "invalid_api_credentials",
    "invalid_message_request",
    "message_assertions",
    "message_client",
    "public_session",
    "report_assertions",
    "report_client",
    "room_assertions",
    "room_client",
    "room_request",
    "schema_registry",
    "settings",
    "valid_api_credentials",
]
