"""Public contact form component."""

from playwright.sync_api import Locator, Page

from restful_booker.models import ContactMessage


class ContactForm:
    """Contact form behavior owned by the home page."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self._root = page.locator("#contact")
        self._name = self._root.get_by_test_id("ContactName")
        self._email = self._root.get_by_test_id("ContactEmail")
        self._phone = self._root.get_by_test_id("ContactPhone")
        self._subject = self._root.get_by_test_id("ContactSubject")
        self._message = self._root.get_by_test_id("ContactDescription")
        self._submit_button = self._root.get_by_role("button", name="Submit", exact=True)

    @property
    def validation_feedback(self) -> Locator:
        """Validation summary displayed after an invalid submission."""

        return self._root.locator(".alert")

    def confirmation(self, text: str) -> Locator:
        """Locate a piece of text in the successful submission confirmation."""

        return self._root.get_by_text(text, exact=False)

    def submit_empty(self) -> None:
        """Submit the untouched form to trigger required-field validation."""

        self._submit_button.click()

    def submit(self, contact_message: ContactMessage) -> None:
        """Fill and submit a valid contact message."""

        self._name.fill(contact_message.name)
        self._email.fill(contact_message.email)
        self._phone.fill(contact_message.phone)
        self._subject.fill(contact_message.subject)
        self._message.fill(contact_message.message)
        self._submit_button.click()
