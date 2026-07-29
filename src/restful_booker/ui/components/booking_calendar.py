"""Reservation calendar component."""

from playwright.sync_api import Locator, Page


class BookingCalendar:
    """Calendar behavior used to select a stay period."""

    def __init__(self, page: Page) -> None:
        self._month_view = page.get_by_role(
            "table",
            name="Month View",
            exact=True,
        ).describe("Reservation calendar month view")

    @property
    def month_view(self) -> Locator:
        """Calendar table for the currently visible month."""

        return self._month_view
