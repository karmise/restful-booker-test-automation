"""UI fixture imports scoped to the UI test suite."""

from collections.abc import Generator

import allure
import pytest
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from playwright.sync_api import Page

from fixtures.ui.assertions import (
    admin_assertions,
    home_assertions,
    reservation_assertions,
)
from fixtures.ui.configuration import configure_page, settings
from fixtures.ui.data import (
    admin_credentials,
    booking_request,
    contact_message,
    double_room,
    invalid_admin_credentials,
    invalid_contact_message,
    invalid_guest_details,
    test_data_factory,
)
from fixtures.ui.pages import admin_page, home_page, reservation_page

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
    "admin_credentials",
    "admin_page",
    "attach_screenshot_on_failure",
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
