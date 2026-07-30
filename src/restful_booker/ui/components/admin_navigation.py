"""Navigation for authenticated administration pages."""

from playwright.sync_api import Locator, Page

from restful_booker.reporting import report_step


class AdminNavigation:
    """Authenticated administration navigation and session controls."""

    def __init__(self, page: Page) -> None:
        self._root = page.get_by_role("navigation").describe("Administration navigation")
        self._logout_button = self._root.get_by_role(
            "button",
            name="Logout",
            exact=True,
        ).describe("Administrator logout button")

    def link(self, name: str) -> Locator:
        """Return a named link from the administration navigation."""

        return self._root.get_by_role(
            "link",
            name=name,
            exact=True,
        ).describe(f"Administration navigation link '{name}'")

    @report_step("Log out from administration")
    def logout(self) -> None:
        """End the current administrator session."""

        self._logout_button.click()

    @report_step("Open an administration section")
    def open_section(self, name: str) -> None:
        """Follow a link from the administration navigation."""

        self.link(name).click()
