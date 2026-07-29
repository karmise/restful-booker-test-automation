"""Assertions for the public home page."""

from playwright.sync_api import expect

from restful_booker.models import ContactMessage, Room
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

    def __init__(self, home_page: HomePage) -> None:
        self._home_page = home_page

    def room_is_available(self, room: Room) -> None:
        """Verify that a seeded room is displayed on the home page."""

        expect(
            self._home_page.room_card(room.name),
            f"Seeded room '{room.name}' should be available on the home page",
        ).to_be_visible()

    def required_contact_errors_are_displayed(self) -> None:
        """Verify the complete required-field validation contract."""

        feedback = self._home_page.contact_form.validation_feedback
        for error in self.required_contact_errors:
            expect(
                feedback,
                f"Contact validation should include: {error}",
            ).to_contain_text(error)

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
