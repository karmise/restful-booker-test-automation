"""Assertions for room details, pricing, and guest validation."""

import re

from playwright.sync_api import Page, expect

from restful_booker.core import Settings
from restful_booker.models import Room, StayPeriod
from restful_booker.reporting import report_step
from restful_booker.ui.pages import ReservationPage


class ReservationAssertions:
    """Business-readable checks for the room reservation page."""

    def __init__(
        self,
        page: Page,
        reservation_page: ReservationPage,
        settings: Settings,
    ) -> None:
        self._page = page
        self._reservation_page = reservation_page
        self._settings = settings

    @report_step("Verify that the selected room reservation page is open")
    def selected_room_is_open(self, room: Room) -> None:
        """Verify navigation from a room card to its reservation page."""

        expect(
            self._page,
            f"Selecting room '{room.name}' should open reservation/{room.room_id}",
        ).to_have_url(
            re.compile(
                rf"^{re.escape(self._settings.base_url)}"
                rf"/reservation/{room.room_id}\?.+$"
            )
        )
        expect(
            self._reservation_page.room_overview.heading(room.room_type),
            f"Reservation page should show type '{room.room_type}' for selected room '{room.name}'",
        ).to_be_visible()

    @report_step("Verify the selected room details")
    def room_details_are_displayed(self, room: Room) -> None:
        """Verify the primary room information and configured features."""

        expect(
            self._reservation_page.room_overview.heading(room.room_type),
            f"Room heading should show type '{room.room_type}' for room '{room.name}'",
        ).to_be_visible()
        expect(
            self._reservation_page.room_overview.hero_image,
            f"The '{room.name}' room should display its primary image",
        ).to_be_visible()
        for feature in room.features:
            expect(
                self._reservation_page.room_overview.feature(feature),
                f"The '{room.name}' room should list the '{feature}' feature",
            ).to_be_visible()

    @report_step("Verify the nightly calculation and final price")
    def price_summary_matches(self, room: Room, stay: StayPeriod) -> None:
        """Verify the nightly calculation and fixed service fees."""

        expected_total = room.nightly_rate * stay.nights + 40
        expect(
            self._reservation_page.booking_panel.price_line(
                nightly_rate=room.nightly_rate,
                nights=stay.nights,
            ),
            "Price summary should multiply the nightly rate by the selected nights",
        ).to_be_visible()
        expect(
            self._reservation_page.booking_panel.total(expected_total),
            "Reservation total should include the room price and £40 fixed fees",
        ).to_be_visible()

    @report_step("Verify required guest-name validation messages")
    def required_guest_name_errors_are_displayed(self) -> None:
        """Verify required first-name and last-name validation."""

        feedback = self._reservation_page.booking_panel.validation_feedback
        expect(
            feedback,
            "Guest validation should require a first name",
        ).to_contain_text("Firstname should not be blank")
        expect(
            feedback,
            "Guest validation should require a last name",
        ).to_contain_text("Lastname should not be blank")

    @report_step("Verify that guest entry is cancelled")
    def guest_entry_is_cancelled(self) -> None:
        """Verify that cancelling restores date selection without the guest form."""

        expect(
            self._reservation_page.booking_panel.first_name_input,
            "Cancelling guest entry should close the guest-details form",
        ).to_be_hidden()
        expect(
            self._reservation_page.calendar.month_view,
            "Cancelling guest entry should restore the reservation calendar",
        ).to_be_visible()

    @report_step("Verify guest contact validation messages")
    def invalid_guest_contact_details_are_reported(self) -> None:
        """Verify email and phone format validation for complete guest details."""

        feedback = self._reservation_page.booking_panel.validation_feedback
        expect(
            feedback,
            "Guest validation should reject a malformed email address",
        ).to_contain_text("must be a well-formed email address")
        expect(
            feedback,
            "Guest validation should reject a phone number shorter than 11 characters",
        ).to_contain_text("size must be between 11 and 21")
