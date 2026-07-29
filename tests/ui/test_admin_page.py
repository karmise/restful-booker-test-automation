"""Administration authentication UI scenarios."""

import pytest

from restful_booker.models import Credentials
from restful_booker.ui.assertions import AdminAssertions
from restful_booker.ui.pages import AdminPage


@pytest.mark.ui
@pytest.mark.regression
def test_invalid_administrator_credentials_are_rejected(
    admin_page: AdminPage,
    admin_assertions: AdminAssertions,
    invalid_admin_credentials: Credentials,
) -> None:
    admin_page.open()

    admin_page.login(invalid_admin_credentials)

    admin_assertions.invalid_credentials_error_is_displayed()


@pytest.mark.ui
@pytest.mark.smoke
def test_administrator_can_sign_in(
    admin_page: AdminPage,
    admin_assertions: AdminAssertions,
    admin_credentials: Credentials,
) -> None:
    admin_page.open()

    admin_page.login(admin_credentials)

    admin_assertions.administrator_is_authenticated()


@pytest.mark.ui
@pytest.mark.regression
def test_protected_rooms_redirect_anonymous_user_to_login(
    admin_page: AdminPage,
    admin_assertions: AdminAssertions,
) -> None:
    admin_page.open_rooms()

    admin_assertions.protected_rooms_require_login()


@pytest.mark.ui
@pytest.mark.regression
def test_administrator_can_open_booking_report(
    admin_page: AdminPage,
    admin_assertions: AdminAssertions,
    admin_credentials: Credentials,
) -> None:
    admin_page.open()
    admin_page.login(admin_credentials)
    admin_assertions.administrator_is_authenticated()

    admin_page.navigation.open_section("Report")

    admin_assertions.booking_report_is_open()


@pytest.mark.ui
@pytest.mark.smoke
def test_logout_removes_access_to_administration(
    admin_page: AdminPage,
    admin_assertions: AdminAssertions,
    admin_credentials: Credentials,
) -> None:
    admin_page.open()
    admin_page.login(admin_credentials)
    admin_assertions.administrator_is_authenticated()

    admin_page.navigation.logout()

    admin_assertions.administrator_is_logged_out()
    admin_page.open_rooms()
    admin_assertions.protected_rooms_require_login()
