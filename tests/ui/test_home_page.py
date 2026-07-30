"""Home page UI scenarios."""

import allure
import pytest

from restful_booker.models import ContactMessage, Room
from restful_booker.ui.assertions import HomeAssertions, ReservationAssertions
from restful_booker.ui.pages import HomePage

pytestmark = [
    allure.epic("Web interface"),
    allure.feature("Home page"),
]


@pytest.mark.ui
@pytest.mark.smoke
@allure.story("Room discovery")
@allure.title("User can open a seeded room")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_opens_a_seeded_room(
    home_page: HomePage,
    home_assertions: HomeAssertions,
    reservation_assertions: ReservationAssertions,
    double_room: Room,
) -> None:
    with allure.step("Open the home page"):
        home_page.open()

    with allure.step("Open the available double room"):
        home_assertions.room_is_available(double_room)
        home_page.open_room(double_room.name)

    with allure.step("Verify that the selected room reservation page is open"):
        reservation_assertions.selected_room_is_open(double_room)


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Contact form validation")
@allure.title("Contact form reports required fields")
@allure.severity(allure.severity_level.NORMAL)
def test_contact_form_reports_required_fields(
    home_page: HomePage,
    home_assertions: HomeAssertions,
) -> None:
    with allure.step("Open the home page"):
        home_page.open()

    with allure.step("Submit an empty contact form"):
        home_page.contact_form.submit_empty()

    with allure.step("Verify required-field validation messages"):
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
    with allure.step("Open the home page"):
        home_page.open()

    with allure.step("Select Contact in the primary navigation"):
        home_page.header.open_section("Contact")

    with allure.step("Verify that the contact section is open"):
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
    with allure.step("Open the home page"):
        home_page.open()

    with allure.step("Submit contact details with invalid email and phone"):
        home_page.contact_form.submit(invalid_contact_message)

    with allure.step("Verify contact format validation messages"):
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
    with allure.step("Open the home page"):
        home_page.open()

    with allure.step("Submit a valid contact message"):
        home_page.contact_form.submit(contact_message)

    with allure.step("Verify that the contact message is accepted"):
        home_assertions.contact_submission_is_confirmed(contact_message)
