"""Home page object."""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from restful_booker.core import Settings
from restful_booker.models import Room
from restful_booker.reporting import report_step
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
        ).describe("Home page welcome heading")
        self._rooms = page.locator("#rooms").describe("Home page rooms section")
        self.header = Header(page)
        self.contact_form = ContactForm(page)

    @report_step("Open the home page")
    def open(self) -> HomePage:
        """Navigate to the public landing page."""

        self._page.goto(
            f"{self._settings.base_url}{self.path}",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )
        return self

    def room_card(self, room: Room) -> Locator:
        """Locate a test-owned room card by its name and canonical URL."""

        room_link = self._rooms.locator(f'a[href="/reservation/{room.room_id}"]')
        return (
            self._rooms.locator(".room-card")
            .filter(has=room_link, has_text=room.name)
            .describe(f"Room card for '{room.name}' (id={room.room_id})")
        )

    @report_step("Open the selected room")
    def open_room(self, room: Room) -> None:
        """Open the reservation page from the test-owned room card."""

        self.room_card(room).get_by_role(
            "link",
            name="Book now",
            exact=True,
        ).describe(f"Book now link for '{room.name}'").click()
