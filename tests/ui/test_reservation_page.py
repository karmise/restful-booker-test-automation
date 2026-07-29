"""Room reservation UI scenarios."""

import pytest
from playwright.sync_api import expect

from restful_booker.models import BookingRequest, Room
from restful_booker.ui.pages import ReservationPage


@pytest.mark.ui
@pytest.mark.smoke
def test_selected_room_details_are_displayed(
    reservation_page: ReservationPage,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )

    expect(reservation_page.room_overview.heading(double_room.name)).to_be_visible()
    expect(reservation_page.room_overview.hero_image).to_be_visible()
    for feature in double_room.features:
        expect(reservation_page.room_overview.feature(feature)).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_price_summary_reflects_selected_stay(
    reservation_page: ReservationPage,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )
    expected_total = double_room.nightly_rate * booking_request.stay.nights + 40

    expect(
        reservation_page.booking_panel.price_line(
            nightly_rate=double_room.nightly_rate,
            nights=booking_request.stay.nights,
        )
    ).to_be_visible()
    expect(reservation_page.booking_panel.total(expected_total)).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_guest_form_reports_required_names(
    reservation_page: ReservationPage,
    booking_request: BookingRequest,
    double_room: Room,
) -> None:
    reservation_page.open(
        room_id=double_room.room_id,
        stay=booking_request.stay,
    )

    reservation_page.booking_panel.open_guest_form()
    reservation_page.booking_panel.submit_empty_guest_form()

    expect(reservation_page.booking_panel.validation_feedback).to_contain_text(
        "Firstname should not be blank"
    )
    expect(reservation_page.booking_panel.validation_feedback).to_contain_text(
        "Lastname should not be blank"
    )
