"""Assertions for the public home page."""

import re

from playwright.sync_api import Page, expect

from restful_booker.core import Settings
from restful_booker.models import ContactMessage, Room
from restful_booker.reporting import report_step
from restful_booker.ui.pages import HomePage


class HomeAssertions:
    """Business-readable checks for rooms and the contact form."""

    required_contact_errors = (
        "Name may not be blank",
        "Email may not be blank",
        "Phone may not be blank",
        "Subject may not be blank",
        "Message may not be blank",
    )

    def __init__(
        self,
        page: Page,
        home_page: HomePage,
        settings: Settings,
    ) -> None:
        self._page = page
        self._home_page = home_page
        self._settings = settings

    @report_step("Verify that the isolated room is available")
    def room_is_available(self, room: Room) -> None:
        """Verify that the test-owned room is displayed on the home page."""

        expect(
            self._home_page.room_card(room),
            f"Isolated room '{room.name}' should be available on the home page",
        ).to_be_visible()

    @report_step("Verify required contact-field validation messages")
    def required_contact_errors_are_displayed(self) -> None:
        """Verify the complete required-field validation contract."""

        feedback = self._home_page.contact_form.validation_feedback
        for error in self.required_contact_errors:
            expect(
                feedback,
                f"Contact validation should include: {error}",
            ).to_contain_text(error)

    @report_step("Verify that the contact section is open")
    def contact_section_is_open(self) -> None:
        """Verify navigation to the contact section of the home page."""

        expect(
            self._page,
            "The Contact navigation link should target the home-page contact section",
        ).to_have_url(
            re.compile(
                rf"^{re.escape(self._settings.base_url)}/?#contact$",
            )
        )
        expect(
            self._home_page.contact_form.heading,
            "The Contact navigation link should reveal the contact form",
        ).to_be_visible()

    @report_step("Verify contact format validation messages")
    def invalid_contact_details_are_reported(self) -> None:
        """Verify email and phone format validation for a complete message."""

        feedback = self._home_page.contact_form.validation_feedback
        expect(
            feedback,
            "Contact validation should reject a malformed email address",
        ).to_contain_text("must be a well-formed email address")
        expect(
            feedback,
            "Contact validation should reject a phone number shorter than 11 characters",
        ).to_contain_text("Phone must be between 11 and 21 characters.")

    @report_step("Verify that the contact message is accepted")
    def contact_submission_is_confirmed(
        self,
        contact_message: ContactMessage,
    ) -> None:
        """Verify the successful contact confirmation content."""

        expect(
            self._home_page.contact_form.confirmation(
                f"Thanks for getting in touch {contact_message.name}!"
            ),
            "A valid contact submission should acknowledge the sender by name",
        ).to_be_visible()
        expect(
            self._home_page.contact_form.confirmation(contact_message.subject),
            "A valid contact submission should repeat the submitted subject",
        ).to_be_visible()
