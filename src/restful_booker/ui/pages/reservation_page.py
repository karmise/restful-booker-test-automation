"""Room reservation page object."""

from __future__ import annotations

import re
from urllib.parse import urlencode

from playwright.sync_api import Page, expect

from restful_booker.core import Settings
from restful_booker.models import StayPeriod
from restful_booker.ui.components import (
    BookingCalendar,
    BookingPanel,
    Header,
    RoomOverview,
)


class ReservationPage:
    """Room details, calendar, pricing, and reservation form."""

    def __init__(self, page: Page, settings: Settings) -> None:
        self._page = page
        self._settings = settings
        self.header = Header(page)
        self.calendar = BookingCalendar(page)
        self.booking_panel = BookingPanel(page)
        self.room_overview = RoomOverview(page)

    def open(self, *, room_id: int, stay: StayPeriod) -> None:
        """Navigate directly to a room with a selected stay period."""

        if room_id <= 0:
            raise ValueError("room_id must be greater than zero")

        query = urlencode(
            {
                "checkin": stay.check_in.isoformat(),
                "checkout": stay.check_out.isoformat(),
            }
        )
        self._page.goto(
            f"{self._settings.base_url}/reservation/{room_id}?{query}",
            wait_until="domcontentloaded",
            timeout=self._settings.navigation_timeout_ms,
        )

    def expect_open_for(self, *, room_id: int, room_name: str) -> None:
        """Verify that the selected room reservation page is open."""

        expect(self._page).to_have_url(
            re.compile(rf"^{re.escape(self._settings.base_url)}/reservation/{room_id}\?.+$"),
        )
        expect(self.room_overview.heading(room_name)).to_be_visible()
