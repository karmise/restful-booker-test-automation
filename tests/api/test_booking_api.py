"""Booking API scenarios."""

from http import HTTPStatus

import pytest

from restful_booker.api.assertions import ApiAssertions, BookingAssertions
from restful_booker.api.clients import BookingClient
from restful_booker.api.testdata import ApiTestDataFactory
from tests.api.fixtures.resources import CreatedBooking, CreatedRoom


@pytest.mark.api
@pytest.mark.smoke
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
