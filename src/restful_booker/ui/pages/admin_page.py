"""Administration page object."""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from restful_booker.contracts.ui import authentication as auth_contract
from restful_booker.contracts.ui import calendar as calendar_contract
from restful_booker.core import Settings
from restful_booker.models import Credentials
from restful_booker.reporting import report_step
from restful_booker.ui.components import AdminNavigation


class AdminPage:
    """Administrator authentication and authenticated shell."""

    path = "/admin"

    def __init__(self, page: Page, settings: Settings) -> None:
        self._page = page
        self._settings = settings
        self._login_heading = page.get_by_role(
            "heading",
            name=auth_contract.LOGIN,
            exact=True,
        ).describe("Administrator login heading")
        self._username = page.get_by_label(
            auth_contract.USERNAME,
            exact=True,
        ).describe("Administrator username input")
        self._password = page.get_by_label(
            auth_contract.PASSWORD,
            exact=True,
        ).describe("Administrator password input")
        self._login_button = page.get_by_role(
            "button",
            name=auth_contract.LOGIN,
            exact=True,
        ).describe("Administrator login submit button")
        self._report_calendar = page.get_by_role(
            "table",
            name=calendar_contract.MONTH_VIEW,
            exact=True,
        ).describe("Administration booking report calendar")
        self.navigation = AdminNavigation(page)

    @property
    def login_heading(self) -> Locator:
        """Administrator login form heading."""

        return self._login_heading

    @property
    def invalid_credentials_feedback(self) -> Locator:
        """Authentication error displayed by the login form."""

        return (
            self._page.get_by_role("alert")
            .filter(has_text=auth_contract.INVALID_CREDENTIALS)
            .describe("Invalid administrator credentials feedback")
        )

    @property
    def report_calendar(self) -> Locator:
        """Calendar displayed on the booking report page."""

        return self._report_calendar

    @report_step("Open the administration login page")
    def open(self) -> AdminPage:
        """Navigate to the administration area."""

        self._page.goto(
            f"{self._settings.base_url}{self.path}",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )
        return self

    @report_step("Open the protected room administration route")
    def open_rooms(self) -> None:
        """Navigate directly to the protected room administration page."""

        self._page.goto(
            f"{self._settings.base_url}/admin/rooms",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )

    @report_step("Submit administrator credentials")
    def login(self, credentials: Credentials) -> None:
        """Submit administrator credentials."""

        self._username.fill(credentials.username)
        self._password.fill(credentials.password)
        self._login_button.click()
