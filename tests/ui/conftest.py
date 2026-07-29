"""UI fixture imports scoped to the UI test suite."""

from tests.ui.fixtures.assertions import (
    admin_assertions,
    home_assertions,
    reservation_assertions,
)
from tests.ui.fixtures.configuration import configure_page, settings
from tests.ui.fixtures.data import (
    admin_credentials,
    booking_request,
    contact_message,
    double_room,
    invalid_admin_credentials,
    invalid_contact_message,
    invalid_guest_details,
    test_data_factory,
)
from tests.ui.fixtures.pages import admin_page, home_page, reservation_page

__all__ = [
    "admin_assertions",
    "admin_credentials",
    "admin_page",
    "booking_request",
    "configure_page",
    "contact_message",
    "double_room",
    "home_assertions",
    "home_page",
    "invalid_admin_credentials",
    "invalid_contact_message",
    "invalid_guest_details",
    "reservation_assertions",
    "reservation_page",
    "settings",
    "test_data_factory",
]
