"""Administration authentication UI scenarios."""

import allure
import pytest

from restful_booker.models import Credentials
from restful_booker.ui.assertions import AdminAssertions
from restful_booker.ui.pages import AdminPage

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("UI tests"),
    allure.sub_suite("Administration"),
    allure.epic("Web interface"),
    allure.feature("Administration"),
]


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Authentication")
@allure.title("Invalid administrator credentials are rejected")
@allure.severity(allure.severity_level.NORMAL)
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
@allure.story("Authentication")
@allure.title("Administrator can sign in")
@allure.severity(allure.severity_level.CRITICAL)
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
@allure.story("Access control")
@allure.title("Protected rooms redirect an anonymous user to login")
@allure.severity(allure.severity_level.CRITICAL)
def test_protected_rooms_redirect_anonymous_user_to_login(
    admin_page: AdminPage,
    admin_assertions: AdminAssertions,
) -> None:
    admin_page.open_rooms()

    admin_assertions.protected_rooms_require_login()


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Navigation")
@allure.title("Administrator can open the booking report")
@allure.severity(allure.severity_level.NORMAL)
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
@allure.story("Authentication")
@allure.title("Logout removes access to administration")
@allure.severity(allure.severity_level.CRITICAL)
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
