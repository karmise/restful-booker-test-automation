"""Unit tests for strict external API contracts."""

from datetime import date

import allure
import pytest

from restful_booker.api.dto import (
    ApiBookingDates,
    AuthRequest,
    BookingCollection,
    BookingRequest,
    RoomResponse,
    TokenResponse,
)
from restful_booker.models import Credentials

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("API contracts"),
    allure.epic("Test framework"),
    allure.feature("DTO contracts"),
]

_BOOKING_ID = 11
_ROOM_ID = 7
_GUEST_FIRST_NAME = "Ada"
_GUEST_LAST_NAME = "Lovelace"
_CHECK_IN = date(2026, 8, 10)
_CHECK_OUT = date(2026, 8, 12)


def test_booking_request_serializes_external_field_names() -> None:
    request = BookingRequest(
        room_id=_ROOM_ID,
        first_name=_GUEST_FIRST_NAME,
        last_name=_GUEST_LAST_NAME,
        deposit_paid=True,
        dates=ApiBookingDates(
            check_in=_CHECK_IN,
            check_out=_CHECK_OUT,
        ),
        email="ada@example.com",
        phone="01234567890",
    )

    assert request.to_payload() == {
        "roomid": _ROOM_ID,
        "firstname": _GUEST_FIRST_NAME,
        "lastname": _GUEST_LAST_NAME,
        "depositpaid": True,
        "bookingdates": {
            "checkin": _CHECK_IN.isoformat(),
            "checkout": _CHECK_OUT.isoformat(),
        },
        "email": "ada@example.com",
        "phone": "01234567890",
    }


def test_room_response_parses_api_payload_into_immutable_types() -> None:
    room = RoomResponse.from_payload(
        {
            "roomid": _ROOM_ID,
            "roomName": "portfolio-room",
            "type": "Suite",
            "accessible": True,
            "image": "/images/room.jpg",
            "description": "A test room",
            "features": ["WiFi", "TV"],
            "roomPrice": 225,
        }
    )

    assert room.room_id == _ROOM_ID
    assert room.features == ("WiFi", "TV")
    assert room.room_price == 225


def test_booking_collection_finds_exact_unique_guest() -> None:
    collection = BookingCollection.from_payload(
        {
            "bookings": [
                {
                    "bookingid": _BOOKING_ID,
                    "roomid": _ROOM_ID,
                    "firstname": _GUEST_FIRST_NAME,
                    "lastname": _GUEST_LAST_NAME,
                    "depositpaid": False,
                    "bookingdates": {
                        "checkin": _CHECK_IN.isoformat(),
                        "checkout": _CHECK_OUT.isoformat(),
                    },
                }
            ]
        }
    )

    booking = collection.find_by_guest(
        first_name=_GUEST_FIRST_NAME,
        last_name=_GUEST_LAST_NAME,
    )

    assert booking.booking_id == _BOOKING_ID
    assert booking.dates.check_in == _CHECK_IN


def test_token_response_rejects_non_string_token() -> None:
    with pytest.raises(TypeError, match="'token' must be a string"):
        TokenResponse.from_payload({"token": 123})


def test_authentication_models_hide_secrets_without_changing_payloads() -> None:
    auth = AuthRequest(username="operator", password="private-password")
    credentials = Credentials(username="operator", password="private-password")
    token = TokenResponse.from_payload({"token": "private-token"})

    assert "private-password" not in repr(auth)
    assert "private-password" not in repr(credentials)
    assert "private-token" not in repr(token)
    assert auth.to_payload() == {"username": "operator", "password": "private-password"}
    assert credentials.password == "private-password"
    assert token.token == "private-token"
