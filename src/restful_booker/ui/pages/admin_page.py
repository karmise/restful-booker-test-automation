"""Administration page object."""

from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect

from restful_booker.core import Settings
from restful_booker.models import Credentials
from restful_booker.ui.components import AdminNavigation


class AdminPage:
    """Administrator authentication and authenticated shell."""

    path = "/admin"

    def __init__(self, page: Page, settings: Settings) -> None:
        self._page = page
        self._settings = settings
        self._login_heading = page.get_by_role(
            "heading",
            name="Login",
            exact=True,
        )
        self._username = page.get_by_label("Username", exact=True)
        self._password = page.get_by_label("Password", exact=True)
        self._login_button = page.get_by_role(
            "button",
            name="Login",
            exact=True,
        )
        self.navigation = AdminNavigation(page)

    @property
    def invalid_credentials_feedback(self) -> Locator:
        """Authentication error displayed by the login form."""

        return self._page.get_by_role("alert").filter(has_text="Invalid credentials")

    def open(self) -> AdminPage:
        """Navigate to the administration area."""

        self._page.goto(
            f"{self._settings.base_url}{self.path}",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )
        expect(self._login_heading).to_be_visible()
        return self

    def open_rooms(self) -> None:
        """Navigate directly to the protected room administration page."""

        self._page.goto(
            f"{self._settings.base_url}/admin/rooms",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )

    def login(self, credentials: Credentials) -> None:
        """Submit administrator credentials."""

        self._username.fill(credentials.username)
        self._password.fill(credentials.password)
        self._login_button.click()

    def expect_authenticated(self) -> None:
        """Verify the authenticated administration shell."""

        expect(self._page).to_have_url(
            re.compile(rf"^{re.escape(self._settings.base_url)}/admin/rooms/?$")
        )
        expect(self.navigation.link("Rooms")).to_be_visible()
        expect(self.navigation.link("Report")).to_be_visible()

    def expect_login_required(self) -> None:
        """Verify that the browser is on the administrator login page."""

        expect(self._page).to_have_url(
            re.compile(rf"^{re.escape(self._settings.base_url)}/admin/?$")
        )
        expect(self._login_heading).to_be_visible()

    def expect_logged_out(self) -> None:
        """Verify the public page reached after logout."""

        expect(self._page).to_have_url(re.compile(rf"^{re.escape(self._settings.base_url)}/?$"))
