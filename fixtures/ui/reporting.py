"""Best-effort browser diagnostics that preserve the original test failure."""

import logging

import allure
from playwright.sync_api import Error, Page

LOGGER = logging.getLogger(__name__)


def attach_failure_screenshot(page: Page) -> None:
    """Capture an open page, tolerating a browser closing during teardown."""

    try:
        if page.is_closed():
            return
        screenshot = page.screenshot(full_page=True, timeout=5_000)
    except Error as error:
        LOGGER.warning("Could not capture browser state at failure: %s", error)
        return
    allure.attach(
        screenshot,
        name="Browser state at failure",
        attachment_type=allure.attachment_type.PNG,
    )
