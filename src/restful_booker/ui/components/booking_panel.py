"""Room booking panel component."""

from playwright.sync_api import Locator, Page


class BookingPanel:
    """Pricing, guest form, and validation inside the booking card."""

    def __init__(self, page: Page) -> None:
        self._root = page.locator(".booking-card")
        self._reserve_button = self._root.get_by_role(
            "button",
            name="Reserve Now",
            exact=True,
        )

    @property
    def validation_feedback(self) -> Locator:
        """Server-side validation summary for guest details."""

        return self._root.get_by_role("alert")

    def price_line(self, *, nightly_rate: int, nights: int) -> Locator:
        """Locate the variable part of the price summary."""

        return self._root.get_by_text(
            f"£{nightly_rate} x {nights} nights",
            exact=True,
        )

    def total(self, amount: int) -> Locator:
        """Locate the calculated total in the price summary."""

        return self._root.get_by_text(f"£{amount}", exact=True)

    def open_guest_form(self) -> None:
        """Move from date selection to the guest-details form."""

        self._reserve_button.click()
        self._root.get_by_label("Firstname", exact=True).wait_for(state="visible")

    def submit_empty_guest_form(self) -> None:
        """Submit the guest form without entering personal data."""

        self._reserve_button.click()
