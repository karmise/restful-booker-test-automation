"""UI runtime configuration fixtures."""

import pytest
from playwright.sync_api import Page, expect

from restful_booker.core import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Load settings once for the complete test session."""

    loaded_settings = Settings.from_env()
    expect.set_options(timeout=loaded_settings.action_timeout_ms)
    return loaded_settings


@pytest.fixture(autouse=True)
def configure_page(page: Page, settings: Settings) -> None:
    """Apply framework timeouts to every Playwright page."""

    page.set_default_timeout(settings.action_timeout_ms)
    page.set_default_navigation_timeout(settings.navigation_timeout_ms)
