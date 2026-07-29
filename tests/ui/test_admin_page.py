"""Administration authentication UI scenarios."""

import pytest
from playwright.sync_api import expect

from restful_booker.models import Credentials
from restful_booker.ui.pages import AdminPage


@pytest.mark.ui
@pytest.mark.regression
def test_invalid_administrator_credentials_are_rejected(
    admin_page: AdminPage,
    invalid_admin_credentials: Credentials,
) -> None:
    admin_page.open()

    admin_page.login(invalid_admin_credentials)

    expect(admin_page.invalid_credentials_feedback).to_have_text("Invalid credentials")


@pytest.mark.ui
@pytest.mark.smoke
def test_administrator_can_sign_in(
    admin_page: AdminPage,
    admin_credentials: Credentials,
) -> None:
    admin_page.open()

    admin_page.login(admin_credentials)

    admin_page.expect_authenticated()


@pytest.mark.ui
@pytest.mark.smoke
def test_logout_removes_access_to_administration(
    admin_page: AdminPage,
    admin_credentials: Credentials,
) -> None:
    admin_page.open()
    admin_page.login(admin_credentials)
    admin_page.expect_authenticated()

    admin_page.navigation.logout()

    admin_page.expect_logged_out()
    admin_page.open_rooms()
    admin_page.expect_login_required()
