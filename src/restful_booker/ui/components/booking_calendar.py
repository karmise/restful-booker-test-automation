"""Reservation calendar component."""

from playwright.sync_api import Locator, Page

from restful_booker.contracts.ui import calendar as calendar_contract


class BookingCalendar:
    """Calendar behavior used to select a stay period."""

    def __init__(self, page: Page) -> None:
        self._month_view = page.get_by_role(
            "table",
            name=calendar_contract.MONTH_VIEW,
            exact=True,
        ).describe("Reservation calendar month view")

    @property
    def month_view(self) -> Locator:
        """Calendar table for the currently visible month."""

        return self._month_view
