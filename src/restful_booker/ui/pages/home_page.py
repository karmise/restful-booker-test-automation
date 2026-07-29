"""Home page object."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from restful_booker.core import Settings
from restful_booker.ui.components import ContactForm, Header


class HomePage:
    """Public landing page and its high-level UI sections."""

    path = "/"

    def __init__(self, page: Page, settings: Settings) -> None:
        self._page = page
        self._settings = settings
        self._heading = page.get_by_role(
            "heading",
            name="Welcome to Shady Meadows B&B",
            exact=True,
        )
        self._rooms = page.locator("#rooms")
        self.header = Header(page)
        self.contact_form = ContactForm(page)

    def open(self) -> HomePage:
        """Navigate to the public landing page."""

        self._page.goto(
            f"{self._settings.base_url}{self.path}",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )
        expect(self._heading).to_be_visible()
        return self

    def room_card(self, room_name: str) -> Locator:
        """Locate a seeded room card by its user-visible name."""

        return self._rooms.locator(".room-card").filter(has_text=room_name)

    def open_room(self, room_name: str) -> None:
        """Open the reservation page from a named room card."""

        self.room_card(room_name).get_by_role(
            "link",
            name="Book now",
            exact=True,
        ).click()
