"""UI assertion object fixtures."""

import pytest
from playwright.sync_api import Page

from restful_booker.core import Settings
from restful_booker.ui.assertions import (
    AdminAssertions,
    HomeAssertions,
    ReservationAssertions,
)
from restful_booker.ui.pages import AdminPage, HomePage, ReservationPage


@pytest.fixture
def home_assertions(
    page: Page,
    home_page: HomePage,
    settings: Settings,
) -> HomeAssertions:
    """Compose assertions for the public home page."""

    return HomeAssertions(page, home_page, settings)


@pytest.fixture
def reservation_assertions(
    page: Page,
    reservation_page: ReservationPage,
    settings: Settings,
) -> ReservationAssertions:
    """Compose assertions for the room reservation page."""

    return ReservationAssertions(page, reservation_page, settings)


@pytest.fixture
def admin_assertions(
    page: Page,
    admin_page: AdminPage,
    settings: Settings,
) -> AdminAssertions:
    """Compose assertions for administrator authentication."""

    return AdminAssertions(page, admin_page, settings)
