"""Booking API scenarios."""

from http import HTTPStatus

import allure
import pytest

from fixtures.api.resources import CreatedBooking, CreatedRoom
from restful_booker.api.assertions import ApiAssertions, BookingAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import BookingClient
from restful_booker.api.dto import BookingResponse
from restful_booker.api.testdata import ApiTestDataFactory

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("API tests"),
    allure.sub_suite("Booking service"),
    allure.epic("REST API"),
    allure.feature("Booking service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Booking creation")
@allure.title("Guest can create a booking for an isolated room")
@allure.severity(allure.severity_level.CRITICAL)
def test_guest_can_create_booking_for_isolated_room(
    created_booking: CreatedBooking,
    api_assertions: ApiAssertions,
    booking_assertions: BookingAssertions,
) -> None:
    api_assertions.has_status(
        created_booking.create_response,
        HTTPStatus.CREATED,
        because="A guest should be able to book an available room",
    )
    api_assertions.has_status(
        created_booking.collection_response,
        HTTPStatus.OK,
        because="The created booking should be discoverable by the administrator",
    )
    api_assertions.matches_schema(created_booking.collection_response, "bookings")
    booking_assertions.created_booking_matches(
        created_booking.booking,
        created_booking.request,
    )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Guest validation")
@allure.title("Booking rejects invalid guest details")
@allure.severity(allure.severity_level.NORMAL)
def test_booking_rejects_invalid_guest_details(
    booking_client: BookingClient,
    api_assertions: ApiAssertions,
    api_test_data_factory: ApiTestDataFactory,
    created_room: CreatedRoom,
) -> None:
    request = api_test_data_factory.booking_with_invalid_guest(room_id=created_room.room.room_id)

    response = booking_client.create_booking(request)

    api_assertions.has_status(
        response,
        HTTPStatus.BAD_REQUEST,
        because="A booking with invalid guest fields must not be persisted",
    )
    api_assertions.contains_error(response, "Firstname should not be blank")
    api_assertions.contains_error(response, "well-formed email")


@pytest.mark.api
@pytest.mark.regression
@allure.story("Date validation")
@allure.title("Booking rejects checkout before check-in")
@allure.severity(allure.severity_level.NORMAL)
def test_booking_rejects_checkout_before_checkin(
    booking_client: BookingClient,
    api_assertions: ApiAssertions,
    api_test_data_factory: ApiTestDataFactory,
    created_room: CreatedRoom,
) -> None:
    request = api_test_data_factory.booking_with_reversed_dates(room_id=created_room.room.room_id)

    response = booking_client.create_booking(request)

    api_assertions.has_status(
        response,
        HTTPStatus.CONFLICT,
        because="Checkout before check-in violates the booking date contract",
    )
    api_assertions.contains_error(response, "Failed to create booking")


@pytest.mark.api
@pytest.mark.regression
@allure.story("Booking authorization")
@allure.title("Anonymous user cannot list room bookings")
@allure.severity(allure.severity_level.CRITICAL)
def test_anonymous_user_cannot_list_room_bookings(
    booking_client: BookingClient,
    api_assertions: ApiAssertions,
    created_room: CreatedRoom,
) -> None:
    response = booking_client.get_bookings_for_room(created_room.room.room_id)

    api_assertions.has_status(
        response,
        HTTPStatus.UNAUTHORIZED,
        because="Booking administration data must not be exposed anonymously",
    )
    api_assertions.contains_error(response, "Authentication required")


@pytest.mark.api
@pytest.mark.regression
@allure.story("Booking discovery")
@allure.title("Administrator can retrieve a booking by identifier")
@allure.severity(allure.severity_level.CRITICAL)
def test_administrator_can_retrieve_booking_by_identifier(
    admin_booking_client: BookingClient,
    api_assertions: ApiAssertions,
    booking_assertions: BookingAssertions,
    created_booking: CreatedBooking,
) -> None:
    response = admin_booking_client.get_booking(created_booking.booking.booking_id)

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="A created booking should be available to an authenticated administrator",
    )
    booking_assertions.created_booking_matches(
        BookingResponse.from_payload(response_json(response)),
        created_booking.request,
    )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Booking authorization")
@allure.title("Anonymous user cannot retrieve a booking by identifier")
@allure.severity(allure.severity_level.CRITICAL)
def test_anonymous_user_cannot_retrieve_booking_by_identifier(
    booking_client: BookingClient,
    api_assertions: ApiAssertions,
    created_booking: CreatedBooking,
) -> None:
    response = booking_client.get_booking(created_booking.booking.booking_id)

    api_assertions.has_status(
        response,
        HTTPStatus.FORBIDDEN,
        because="Guest personal data must not be exposed without administrator authentication",
    )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Booking conflict")
@allure.title("Overlapping booking for the same room is rejected")
@allure.severity(allure.severity_level.CRITICAL)
def test_overlapping_booking_for_same_room_is_rejected(
    booking_client: BookingClient,
    api_assertions: ApiAssertions,
    api_test_data_factory: ApiTestDataFactory,
    created_booking: CreatedBooking,
) -> None:
    request = api_test_data_factory.overlapping_booking(created_booking.request)

    response = booking_client.create_booking(request)

    api_assertions.has_status(
        response,
        HTTPStatus.CONFLICT,
        because="The same room must not be double-booked for overlapping dates",
    )
    api_assertions.contains_error(response, "Failed to create booking")
