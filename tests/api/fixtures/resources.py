"""Created-resource fixtures with guaranteed reverse-order cleanup."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

import allure
import pytest
from requests import Response

from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import BookingClient, MessageClient, RoomClient
from restful_booker.api.dto import (
    BookingCollection,
    BookingRequest,
    BookingResponse,
    MessageCollection,
    MessageRequest,
    MessageSummary,
    RoomCollection,
    RoomRequest,
    RoomResponse,
)
from restful_booker.api.testdata import ApiTestDataFactory


@dataclass(frozen=True, slots=True)
class CreatedRoom:
    request: RoomRequest
    create_response: Response
    collection_response: Response
    room: RoomResponse


@dataclass(frozen=True, slots=True)
class CreatedBooking:
    request: BookingRequest
    create_response: Response
    collection_response: Response
    booking: BookingResponse


@dataclass(frozen=True, slots=True)
class CreatedMessage:
    request: MessageRequest
    create_response: Response
    collection_response: Response
    message: MessageSummary


@pytest.fixture
@allure.title("Create an isolated API room")
def created_room(
    admin_room_client: RoomClient,
    room_client: RoomClient,
    room_request: RoomRequest,
) -> Iterator[CreatedRoom]:
    """Create a unique room and always remove it after dependent resources."""

    with allure.step("Create a unique room as administrator"):
        create_response = admin_room_client.create_room(room_request)
        _require_status(create_response, 200, resource="room creation")

    with allure.step("Discover the created room in the public collection"):
        collection_response = room_client.get_rooms()
        _require_status(collection_response, 200, resource="room discovery")
        room = RoomCollection.from_payload(response_json(collection_response)).find_by_name(
            room_request.room_name
        )

    try:
        yield CreatedRoom(
            request=room_request,
            create_response=create_response,
            collection_response=collection_response,
            room=room,
        )
    finally:
        with allure.step("Delete the isolated room"):
            delete_response = admin_room_client.delete_room(room.room_id)
            _require_status(delete_response, 202, resource=f"room {room.room_id} cleanup")


@pytest.fixture
@allure.title("Create an isolated API booking")
def created_booking(
    booking_client: BookingClient,
    admin_booking_client: BookingClient,
    created_room: CreatedRoom,
    api_test_data_factory: ApiTestDataFactory,
) -> Iterator[CreatedBooking]:
    """Create a booking for the test room and delete it before room cleanup."""

    with allure.step("Create a booking for the isolated room"):
        request = api_test_data_factory.booking_request(
            room_id=created_room.room.room_id,
        )
        create_response = booking_client.create_booking(request)
        _require_status(create_response, 201, resource="booking creation")

    with allure.step("Discover the created booking as administrator"):
        collection_response = admin_booking_client.get_bookings_for_room(created_room.room.room_id)
        _require_status(collection_response, 200, resource="booking discovery")
        booking = BookingCollection.from_payload(response_json(collection_response)).find_by_guest(
            first_name=request.first_name,
            last_name=request.last_name,
        )

    try:
        yield CreatedBooking(
            request=request,
            create_response=create_response,
            collection_response=collection_response,
            booking=booking,
        )
    finally:
        with allure.step("Delete the isolated booking"):
            delete_response = admin_booking_client.delete_booking(booking.booking_id)
            _require_status(
                delete_response,
                202,
                resource=f"booking {booking.booking_id} cleanup",
            )


@pytest.fixture
@allure.title("Create an isolated API contact message")
def created_message(
    message_client: MessageClient,
    admin_message_client: MessageClient,
    api_test_data_factory: ApiTestDataFactory,
) -> Iterator[CreatedMessage]:
    """Create a unique contact message and always delete it."""

    with allure.step("Create a unique public contact message"):
        request = api_test_data_factory.message_request()
        create_response = message_client.create_message(request)
        _require_status(create_response, 200, resource="message creation")

    with allure.step("Discover the created message in administration"):
        collection_response = message_client.get_messages()
        _require_status(collection_response, 200, resource="message discovery")
        message = MessageCollection.from_payload(
            response_json(collection_response)
        ).find_by_subject(request.subject)

    try:
        yield CreatedMessage(
            request=request,
            create_response=create_response,
            collection_response=collection_response,
            message=message,
        )
    finally:
        with allure.step("Delete the isolated contact message"):
            delete_response = admin_message_client.delete_message(message.message_id)
            _require_status(
                delete_response,
                202,
                resource=f"message {message.message_id} cleanup",
            )


def _require_status(response: Response, expected: int, *, resource: str) -> None:
    if response.status_code != expected:
        raise RuntimeError(
            f"API fixture failed during {resource}: expected {expected}, "
            f"got {response.status_code}. Body: {response.text}"
        )
