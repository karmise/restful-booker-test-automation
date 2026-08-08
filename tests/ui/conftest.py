"""UI fixture imports scoped to the UI test suite."""

from collections.abc import Generator

import allure
import pytest
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from playwright.sync_api import Page

from fixtures.api.clients import (
    admin_booking_client,
    admin_message_client,
    admin_room_client,
    authenticated_session,
    public_session,
    room_client,
)
from fixtures.api.data import api_test_data_factory, room_request
from fixtures.api.resources import api_resource_lifecycle, created_room
from fixtures.ui.assertions import (
    admin_assertions,
    home_assertions,
    reservation_assertions,
)
from fixtures.ui.configuration import configure_page, settings
from fixtures.ui.data import (
    admin_credentials,
    booking_request,
    contact_message_data,
    invalid_admin_credentials,
    invalid_contact_message,
    invalid_guest_details,
    public_double_room,
    test_data_factory,
)
from fixtures.ui.pages import admin_page, home_page, reservation_page
from fixtures.ui.resources import contact_message, isolated_room

_PHASE_REPORTS = pytest.StashKey[dict[str, TestReport]]()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: Item,
    call: CallInfo[None],
) -> Generator[None, TestReport, TestReport]:
    """Keep the phase result available to reporting fixtures."""

    report = yield
    item.stash.setdefault(_PHASE_REPORTS, {})[report.when] = report
    return report


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(
    page: Page,
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """Attach the final browser state to a failed Allure result."""

    yield
    call_report = request.node.stash.get(_PHASE_REPORTS, {}).get("call")
    if call_report is not None and call_report.failed and not page.is_closed():
        allure.attach(
            page.screenshot(full_page=True),
            name="Browser state at failure",
            attachment_type=allure.attachment_type.PNG,
        )


__all__ = [
    "admin_assertions",
    "admin_booking_client",
    "admin_credentials",
    "admin_message_client",
    "admin_page",
    "admin_room_client",
    "api_resource_lifecycle",
    "api_test_data_factory",
    "attach_screenshot_on_failure",
    "authenticated_session",
    "booking_request",
    "configure_page",
    "contact_message",
    "contact_message_data",
    "created_room",
    "home_assertions",
    "home_page",
    "invalid_admin_credentials",
    "invalid_contact_message",
    "invalid_guest_details",
    "isolated_room",
    "public_double_room",
    "public_session",
    "reservation_assertions",
    "reservation_page",
    "room_client",
    "room_request",
    "settings",
    "test_data_factory",
]
