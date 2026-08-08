"""Room information component."""

from playwright.sync_api import Locator, Page


class RoomOverview:
    """User-visible room title, image, and feature list."""

    def __init__(self, page: Page) -> None:
        self._page = page

    def heading(self, room_type: str) -> Locator:
        """Locate the primary room heading."""

        return self._page.get_by_role(
            "heading",
            name=f"{room_type} Room",
            exact=True,
        ).describe(f"Primary heading for '{room_type}' room type")

    @property
    def hero_image(self) -> Locator:
        """Primary room image."""

        return self._page.get_by_role(
            "img",
            name="Room Image",
            exact=True,
        ).describe("Primary room image")

    def feature(self, name: str) -> Locator:
        """Locate a named room feature."""

        return self._page.get_by_text(
            name,
            exact=True,
        ).describe(f"Room feature '{name}'")
