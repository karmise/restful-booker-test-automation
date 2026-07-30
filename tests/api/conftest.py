"""API fixture imports scoped to the API test suite."""

from fixtures.api.assertions import (
    api_assertions,
    auth_assertions,
    booking_assertions,
    branding_assertions,
    message_assertions,
    report_assertions,
    room_assertions,
    schema_registry,
)
from fixtures.api.clients import (
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
from fixtures.api.configuration import settings
from fixtures.api.data import (
    api_test_data_factory,
    invalid_api_credentials,
    invalid_message_request,
    missing_resource_id,
    room_request,
    unknown_authentication_token,
    valid_api_credentials,
)
from fixtures.api.resources import (
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
    "missing_resource_id",
    "public_session",
    "report_assertions",
    "report_client",
    "room_assertions",
    "room_client",
    "room_request",
    "schema_registry",
    "settings",
    "unknown_authentication_token",
    "valid_api_credentials",
]
