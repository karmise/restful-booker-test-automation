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
from restful_booker.api.resource_lifecycle import ApiResourceLifecycle
from restful_booker.api.testdata import ApiTestDataFactory


@dataclass(frozen=True, slots=True)
class CreatedRoom:
    request: RoomRequest
    room: RoomResponse


@dataclass(frozen=True, slots=True)
class CreatedBooking:
    request: BookingRequest
    booking: BookingResponse


@dataclass(frozen=True, slots=True)
class CreatedMessage:
    request: MessageRequest
    message: MessageSummary


@pytest.fixture
@allure.title("Manage test-owned API resources")
def api_resource_lifecycle(
    room_client: RoomClient,
    admin_room_client: RoomClient,
    admin_booking_client: BookingClient,
    admin_message_client: MessageClient,
) -> Iterator[ApiResourceLifecycle]:
    """Clean up every resource registered by the current test."""

    lifecycle = ApiResourceLifecycle(
        room_client=room_client,
        admin_room_client=admin_room_client,
        admin_booking_client=admin_booking_client,
        admin_message_client=admin_message_client,
    )
    yield lifecycle
    lifecycle.cleanup()


@pytest.fixture
@allure.title("Create an isolated API room")
def created_room(
    admin_room_client: RoomClient,
    room_client: RoomClient,
    room_request: RoomRequest,
    api_resource_lifecycle: ApiResourceLifecycle,
) -> CreatedRoom:
    """Create a unique room and always remove it after dependent resources."""

    api_resource_lifecycle.track_room(room_name=room_request.room_name)
    create_response = admin_room_client.create_room(room_request)
    _require_status(create_response, 200, resource="room creation")

    collection_response = room_client.get_rooms()
    _require_status(collection_response, 200, resource="room discovery")
    room = RoomCollection.from_payload(response_json(collection_response)).find_by_name(
        room_request.room_name
    )
    api_resource_lifecycle.track_room(
        room_name=room_request.room_name,
        room_id=room.room_id,
    )

    return CreatedRoom(request=room_request, room=room)


@pytest.fixture
@allure.title("Create an isolated API booking")
def created_booking(
    booking_client: BookingClient,
    admin_booking_client: BookingClient,
    created_room: CreatedRoom,
    api_test_data_factory: ApiTestDataFactory,
    api_resource_lifecycle: ApiResourceLifecycle,
) -> CreatedBooking:
    """Create a booking for the test room and delete it before room cleanup."""

    request = api_test_data_factory.booking_request(
        room_id=created_room.room.room_id,
    )
    api_resource_lifecycle.track_booking(
        room_id=request.room_id,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    create_response = booking_client.create_booking(request)
    _require_status(create_response, 201, resource="booking creation")

    collection_response = admin_booking_client.get_bookings_for_room(created_room.room.room_id)
    _require_status(collection_response, 200, resource="booking discovery")
    booking = BookingCollection.from_payload(response_json(collection_response)).find_by_guest(
        first_name=request.first_name,
        last_name=request.last_name,
    )
    api_resource_lifecycle.track_booking(
        room_id=request.room_id,
        first_name=request.first_name,
        last_name=request.last_name,
        booking_id=booking.booking_id,
    )

    return CreatedBooking(request=request, booking=booking)


@pytest.fixture
@allure.title("Create an isolated API contact message")
def created_message(
    message_client: MessageClient,
    admin_message_client: MessageClient,
    api_test_data_factory: ApiTestDataFactory,
    api_resource_lifecycle: ApiResourceLifecycle,
) -> CreatedMessage:
    """Create a unique contact message and always delete it."""

    request = api_test_data_factory.message_request()
    api_resource_lifecycle.track_message(subject=request.subject)
    create_response = message_client.create_message(request)
    _require_status(create_response, 200, resource="message creation")

    collection_response = admin_message_client.get_messages()
    _require_status(collection_response, 200, resource="message discovery")
    message = MessageCollection.from_payload(response_json(collection_response)).find_by_subject(
        request.subject
    )
    api_resource_lifecycle.track_message(
        subject=request.subject,
        message_id=message.message_id,
    )

    return CreatedMessage(request=request, message=message)


def _require_status(response: Response, expected: int, *, resource: str) -> None:
    if response.status_code != expected:
        raise RuntimeError(
            f"API fixture failed during {resource}: expected {expected}, "
            f"got {response.status_code}. Body: {response.text}"
        )
