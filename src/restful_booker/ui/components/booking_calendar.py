"""Reservation calendar component."""

from playwright.sync_api import Page


class BookingCalendar:
    """Calendar behavior used to select a stay period."""

    def __init__(self, page: Page) -> None:
        self._page = page
