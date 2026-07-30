"""UI page object fixtures."""

import pytest
from playwright.sync_api import Page

from restful_booker.core import Settings
from restful_booker.ui.pages import AdminPage, HomePage, ReservationPage


@pytest.fixture
def home_page(page: Page, settings: Settings) -> HomePage:
    """Compose the home page object for a test."""

    return HomePage(page, settings)


@pytest.fixture
def reservation_page(page: Page, settings: Settings) -> ReservationPage:
    """Compose the reservation page object for a test."""

    return ReservationPage(page, settings)


@pytest.fixture
def admin_page(page: Page, settings: Settings) -> AdminPage:
    """Compose the administration page object for a test."""

    return AdminPage(page, settings)
