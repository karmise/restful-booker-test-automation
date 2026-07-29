"""Room reservation UI scenarios."""

import pytest

from restful_booker.models import BookingRequest, GuestDetails, Room
from restful_booker.ui.assertions import ReservationAssertions
from restful_booker.ui.pages import ReservationPage


@pytest.mark.ui
@pytest.mark.smoke
def test_selected_room_details_are_displayed(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )

    reservation_assertions.room_details_are_displayed(double_room)


@pytest.mark.ui
@pytest.mark.regression
def test_price_summary_reflects_selected_stay(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )
    reservation_assertions.price_summary_matches(
        double_room,
        booking_request.stay,
    )


@pytest.mark.ui
@pytest.mark.regression
def test_guest_form_reports_required_names(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )

    reservation_page.booking_panel.open_guest_form()
    reservation_page.booking_panel.submit_empty_guest_form()

    reservation_assertions.required_guest_name_errors_are_displayed()


@pytest.mark.ui
@pytest.mark.regression
def test_user_can_cancel_guest_details_entry(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )
    reservation_page.booking_panel.open_guest_form()

    reservation_page.booking_panel.cancel_guest_form()

    reservation_assertions.guest_entry_is_cancelled()


@pytest.mark.ui
@pytest.mark.regression
def test_guest_form_reports_invalid_email_and_phone(
    reservation_page: ReservationPage,
    reservation_assertions: ReservationAssertions,
    booking_request: BookingRequest,
    invalid_guest_details: GuestDetails,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )
    reservation_page.booking_panel.open_guest_form()

    reservation_page.booking_panel.submit_guest_details(invalid_guest_details)

    reservation_assertions.invalid_guest_contact_details_are_reported()
