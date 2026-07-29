"""Room information component."""

from playwright.sync_api import Locator, Page


class RoomOverview:
    """User-visible room title, image, and feature list."""

    def __init__(self, page: Page) -> None:
        self._page = page

    def heading(self, room_name: str) -> Locator:
        """Locate the primary room heading."""

        return self._page.get_by_role(
            "heading",
            name=f"{room_name} Room",
            exact=True,
        )

    @property
    def hero_image(self) -> Locator:
        """Primary room image."""

        return self._page.get_by_role("img", name="Room Image", exact=True)

    def feature(self, name: str) -> Locator:
        """Locate a named room feature."""

        return self._page.get_by_text(name, exact=True)
