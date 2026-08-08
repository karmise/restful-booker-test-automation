"""Home page UI scenarios."""

import allure
import pytest

from restful_booker.models import ContactMessage, Room
from restful_booker.ui.assertions import HomeAssertions, ReservationAssertions
from restful_booker.ui.pages import HomePage

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("UI tests"),
    allure.sub_suite("Home page"),
    allure.epic("Web interface"),
    allure.feature("Home page"),
]


@pytest.mark.ui
@pytest.mark.smoke
@allure.story("Room discovery")
@allure.title("User can open an isolated room")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_opens_an_isolated_room(
    home_page: HomePage,
    home_assertions: HomeAssertions,
    reservation_assertions: ReservationAssertions,
    isolated_room: Room,
) -> None:
    home_page.open()

    home_assertions.room_is_available(isolated_room)
    home_page.open_room(isolated_room)

    reservation_assertions.selected_room_is_open(isolated_room)


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Contact form validation")
@allure.title("Contact form reports required fields")
@allure.severity(allure.severity_level.NORMAL)
def test_contact_form_reports_required_fields(
    home_page: HomePage,
    home_assertions: HomeAssertions,
) -> None:
    home_page.open()

    home_page.contact_form.submit_empty()

    home_assertions.required_contact_errors_are_displayed()


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Navigation")
@allure.title("Primary navigation opens the contact section")
@allure.severity(allure.severity_level.NORMAL)
def test_primary_navigation_opens_contact_section(
    home_page: HomePage,
    home_assertions: HomeAssertions,
) -> None:
    home_page.open()

    home_page.header.open_section("Contact")

    home_assertions.contact_section_is_open()


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Contact form validation")
@allure.title("Contact form reports an invalid email and phone")
@allure.severity(allure.severity_level.NORMAL)
def test_contact_form_reports_invalid_email_and_phone(
    home_page: HomePage,
    home_assertions: HomeAssertions,
    invalid_contact_message: ContactMessage,
) -> None:
    home_page.open()

    home_page.contact_form.submit(invalid_contact_message)

    home_assertions.invalid_contact_details_are_reported()


@pytest.mark.ui
@pytest.mark.smoke
@allure.story("Contact form submission")
@allure.title("User can submit a valid contact message")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_submits_a_valid_contact_message(
    home_page: HomePage,
    home_assertions: HomeAssertions,
    contact_message: ContactMessage,
) -> None:
    home_page.open()

    home_page.contact_form.submit(contact_message)

    home_assertions.contact_submission_is_confirmed(contact_message)
