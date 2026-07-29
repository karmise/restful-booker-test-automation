"""Assertions for administrator authentication and authorization."""

import re

from playwright.sync_api import Page, expect

from restful_booker.core import Settings
from restful_booker.ui.pages import AdminPage


class AdminAssertions:
    """Business-readable checks for the administration area."""

    def __init__(
        self,
        page: Page,
        admin_page: AdminPage,
        settings: Settings,
    ) -> None:
        self._page = page
        self._admin_page = admin_page
        self._settings = settings

    def invalid_credentials_error_is_displayed(self) -> None:
        """Verify that invalid credentials produce a user-facing error."""

        expect(
            self._admin_page.invalid_credentials_feedback,
            "Invalid administrator credentials should show an authentication error",
        ).to_have_text("Invalid credentials")

    def administrator_is_authenticated(self) -> None:
        """Verify the authenticated administrator shell and destination."""

        expect(
            self._page,
            "A successful administrator login should open the rooms page",
        ).to_have_url(re.compile(rf"^{re.escape(self._settings.base_url)}/admin/rooms/?$"))
        expect(
            self._admin_page.navigation.link("Rooms"),
            "Authenticated navigation should contain the Rooms link",
        ).to_be_visible()
        expect(
            self._admin_page.navigation.link("Report"),
            "Authenticated navigation should contain the Report link",
        ).to_be_visible()

    def administrator_is_logged_out(self) -> None:
        """Verify that logout returns the user to the public page."""

        expect(
            self._page,
            "Logging out should return the administrator to the public page",
        ).to_have_url(re.compile(rf"^{re.escape(self._settings.base_url)}/?$"))

    def protected_rooms_require_login(self) -> None:
        """Verify that a logged-out user cannot reopen protected rooms."""

        expect(
            self._page,
            "A logged-out user should be redirected to the administrator login page",
        ).to_have_url(re.compile(rf"^{re.escape(self._settings.base_url)}/admin/?$"))
        expect(
            self._admin_page.login_heading,
            "The administrator login form should be visible after redirect",
        ).to_be_visible()
