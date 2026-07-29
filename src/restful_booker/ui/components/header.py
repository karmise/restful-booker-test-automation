"""Primary site navigation component."""

from playwright.sync_api import Locator, Page


class Header:
    """Navigation shared by public application pages."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self._root = page.get_by_role("navigation")

    def link(self, name: str) -> Locator:
        """Return a uniquely named link from the primary navigation."""

        return self._root.get_by_role("link", name=name, exact=True)

    def open_section(self, name: str) -> None:
        """Follow a link from the primary navigation."""

        self.link(name).click()
