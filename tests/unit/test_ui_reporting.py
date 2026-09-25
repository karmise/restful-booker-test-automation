"""Browser diagnostics must not replace the original failure."""

from typing import cast
from unittest.mock import Mock

import allure
import pytest
from playwright.sync_api import Error, Page

from fixtures.ui import reporting

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Browser diagnostics"),
    allure.epic("Test framework"),
    allure.feature("Browser diagnostics"),
]


def test_screenshot_is_attached_with_a_bounded_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    page = Mock(spec=Page)
    page.is_closed.return_value = False
    page.screenshot.return_value = b"image"
    attach = Mock()
    monkeypatch.setattr(reporting.allure, "attach", attach)

    reporting.attach_failure_screenshot(cast(Page, page))

    page.screenshot.assert_called_once_with(full_page=True, timeout=5_000)
    assert attach.call_args.args == (b"image",)


def test_screenshot_failure_preserves_test_failure(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    page = Mock(spec=Page)
    page.is_closed.return_value = False
    page.screenshot.side_effect = Error("Browser closed during capture")
    attach = Mock()
    monkeypatch.setattr(reporting.allure, "attach", attach)

    reporting.attach_failure_screenshot(cast(Page, page))

    assert "Could not capture browser state" in caplog.text
    attach.assert_not_called()


def test_closed_page_is_not_captured() -> None:
    page = Mock(spec=Page)
    page.is_closed.return_value = True

    reporting.attach_failure_screenshot(cast(Page, page))

    page.screenshot.assert_not_called()
