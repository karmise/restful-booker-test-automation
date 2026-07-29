"""Room booking panel component."""

from playwright.sync_api import Locator, Page

from restful_booker.models import GuestDetails


class BookingPanel:
    """Pricing, guest form, and validation inside the booking card."""

    def __init__(self, page: Page) -> None:
        self._root = page.locator(".booking-card").describe("Room booking panel")
        self._reserve_button = self._root.get_by_role(
            "button",
            name="Reserve Now",
            exact=True,
        ).describe("Reserve Now button")
        self._cancel_button = self._root.get_by_role(
            "button",
            name="Cancel",
            exact=True,
        ).describe("Cancel guest details button")
        self._first_name = self._root.get_by_label(
            "Firstname",
            exact=True,
        ).describe("Guest first name input")
        self._last_name = self._root.get_by_label(
            "Lastname",
            exact=True,
        ).describe("Guest last name input")
        self._email = self._root.get_by_label(
            "Email",
            exact=True,
        ).describe("Guest email input")
        self._phone = self._root.get_by_label(
            "Phone",
            exact=True,
        ).describe("Guest phone input")

    @property
    def first_name_input(self) -> Locator:
        """First input displayed when the guest form is open."""

        return self._first_name

    @property
    def validation_feedback(self) -> Locator:
        """Server-side validation summary for guest details."""

        return self._root.get_by_role("alert").describe("Guest details validation feedback")

    def price_line(self, *, nightly_rate: int, nights: int) -> Locator:
        """Locate the variable part of the price summary."""

        return self._root.get_by_text(
            f"£{nightly_rate} x {nights} nights",
            exact=True,
        ).describe(f"Price line for £{nightly_rate} across {nights} nights")

    def total(self, amount: int) -> Locator:
        """Locate the calculated total in the price summary."""

        return self._root.get_by_text(
            f"£{amount}",
            exact=True,
        ).describe(f"Reservation total £{amount}")

    def open_guest_form(self) -> None:
        """Move from date selection to the guest-details form."""

        self._reserve_button.click()
        self._first_name.wait_for(state="visible")

    def cancel_guest_form(self) -> None:
        """Discard guest entry and return to date selection."""

        self._cancel_button.click()

    def submit_empty_guest_form(self) -> None:
        """Submit the guest form without entering personal data."""

        self._reserve_button.click()

    def submit_guest_details(self, guest: GuestDetails) -> None:
        """Fill and submit the currently open guest-details form."""

        self._first_name.fill(guest.first_name)
        self._last_name.fill(guest.last_name)
        self._email.fill(guest.email)
        self._phone.fill(guest.phone)
        self._reserve_button.click()
