"""Public contact form component."""

from playwright.sync_api import Locator, Page

from restful_booker.models import ContactMessage
from restful_booker.reporting import report_step


class ContactForm:
    """Contact form behavior owned by the home page."""

    def __init__(self, page: Page) -> None:
        self._root = page.locator("#contact").describe("Public contact section")
        self._heading = self._root.get_by_role(
            "heading",
            name="Send Us a Message",
            exact=True,
        ).describe("Contact form section heading")
        self._name = self._root.get_by_test_id("ContactName").describe("Contact name input")
        self._email = self._root.get_by_test_id("ContactEmail").describe("Contact email input")
        self._phone = self._root.get_by_test_id("ContactPhone").describe("Contact phone input")
        self._subject = self._root.get_by_test_id("ContactSubject").describe(
            "Contact subject input"
        )
        self._message = self._root.get_by_test_id("ContactDescription").describe(
            "Contact message input"
        )
        self._submit_button = self._root.get_by_role(
            "button",
            name="Submit",
            exact=True,
        ).describe("Contact form submit button")

    @property
    def heading(self) -> Locator:
        """Heading that identifies the public contact form."""

        return self._heading

    @property
    def validation_feedback(self) -> Locator:
        """Validation summary displayed after an invalid submission."""

        return self._root.locator(".alert").describe("Contact form validation feedback")

    def confirmation(self, text: str) -> Locator:
        """Locate a piece of text in the successful submission confirmation."""

        return self._root.get_by_text(
            text,
            exact=False,
        ).describe(f"Contact confirmation containing '{text}'")

    @report_step("Submit an empty contact form")
    def submit_empty(self) -> None:
        """Submit the untouched form to trigger required-field validation."""

        self._submit_button.click()

    @report_step("Submit a contact message")
    def submit(self, contact_message: ContactMessage) -> None:
        """Fill and submit a valid contact message."""

        self._name.fill(contact_message.name)
        self._email.fill(contact_message.email)
        self._phone.fill(contact_message.phone)
        self._subject.fill(contact_message.subject)
        self._message.fill(contact_message.message)
        self._submit_button.click()
