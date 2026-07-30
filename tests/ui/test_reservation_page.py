"""Room reservation UI scenarios."""

import allure
import pytest

from restful_booker.models import BookingRequest, GuestDetails, Room
from restful_booker.ui.assertions import ReservationAssertions
from restful_booker.ui.pages import ReservationPage

pytestmark = [
    allure.epic("Web interface"),
    allure.feature("Room reservation"),
]


@pytest.mark.ui
@pytest.mark.smoke
@allure.story("Room details")
@allure.title("Selected room details are displayed")
@allure.severity(allure.severity_level.CRITICAL)
def test_selected_room_details_are_displayed(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    with allure.step("Open the selected room for the requested stay"):
        reservation_page.open(
            room_id=double_room.room_id,
            stay=booking_request.stay,
        )

    with allure.step("Verify the room description, image, and features"):
        reservation_assertions.room_details_are_displayed(double_room)


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Price calculation")
@allure.title("Price summary reflects the selected stay")
@allure.severity(allure.severity_level.NORMAL)
def test_price_summary_reflects_selected_stay(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    with allure.step("Open the selected room for the requested stay"):
        reservation_page.open(
            room_id=double_room.room_id,
            stay=booking_request.stay,
        )

    with allure.step("Verify the nightly calculation and final price"):
        reservation_assertions.price_summary_matches(
            double_room,
            booking_request.stay,
        )


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Guest details validation")
@allure.title("Guest form reports required names")
@allure.severity(allure.severity_level.NORMAL)
def test_guest_form_reports_required_names(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    with allure.step("Open the selected room for the requested stay"):
        reservation_page.open(
            room_id=double_room.room_id,
            stay=booking_request.stay,
        )

    with allure.step("Submit an empty guest-details form"):
        reservation_page.booking_panel.open_guest_form()
        reservation_page.booking_panel.submit_empty_guest_form()

    with allure.step("Verify required guest-name validation messages"):
        reservation_assertions.required_guest_name_errors_are_displayed()


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Guest details entry")
@allure.title("User can cancel guest details entry")
@allure.severity(allure.severity_level.NORMAL)
def test_user_can_cancel_guest_details_entry(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    with allure.step("Open the guest-details form for the selected stay"):
        reservation_page.open(
            room_id=double_room.room_id,
            stay=booking_request.stay,
        )
        reservation_page.booking_panel.open_guest_form()

    with allure.step("Cancel guest details entry"):
        reservation_page.booking_panel.cancel_guest_form()

    with allure.step("Verify that the reservation calendar is restored"):
        reservation_assertions.guest_entry_is_cancelled()


@pytest.mark.ui
@pytest.mark.regression
@allure.story("Guest details validation")
@allure.title("Guest form reports an invalid email and phone")
@allure.severity(allure.severity_level.NORMAL)
def test_guest_form_reports_invalid_email_and_phone(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    invalid_guest_details: GuestDetails,
    double_room: Room,
) -> None:
    with allure.step("Open the guest-details form for the selected stay"):
        reservation_page.open(
            room_id=double_room.room_id,
            stay=booking_request.stay,
        )
        reservation_page.booking_panel.open_guest_form()

    with allure.step("Submit guest details with invalid email and phone"):
        reservation_page.booking_panel.submit_guest_details(invalid_guest_details)

    with allure.step("Verify guest contact validation messages"):
        reservation_assertions.invalid_guest_contact_details_are_reported()
