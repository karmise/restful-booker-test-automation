"""Unit tests for test-resource cleanup orchestration."""

import json
from typing import cast
from unittest.mock import Mock

import allure
import pytest
from requests import Response

from restful_booker.api.clients import BookingClient, MessageClient, RoomClient
from restful_booker.api.resource_lifecycle import (
    ApiResourceLifecycle,
    ResourceCleanupError,
)

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Resource lifecycle"),
    allure.epic("Test framework"),
    allure.feature("Test-data cleanup"),
]


def test_cleanup_rediscovers_room_when_setup_failed_before_id_was_known() -> None:
    room_client = Mock(spec=RoomClient)
    room_client.get_rooms.return_value = _json_response(
        200,
        {"rooms": [{"roomid": 42, "roomName": "api-unique"}]},
    )
    admin_room_client = Mock(spec=RoomClient)
    admin_room_client.delete_room.return_value = _json_response(202, {})
    lifecycle = _lifecycle(
        room_client=room_client,
        admin_room_client=admin_room_client,
    )
    lifecycle.track_room(room_name="api-unique")

    lifecycle.cleanup()

    admin_room_client.delete_room.assert_called_once_with(42)


def test_cleanup_removes_resources_in_reverse_creation_order() -> None:
    deletion_order: list[str] = []
    admin_room_client = Mock(spec=RoomClient)
    admin_room_client.delete_room.side_effect = lambda room_id: _record_deletion(
        deletion_order,
        f"room:{room_id}",
    )
    admin_booking_client = Mock(spec=BookingClient)
    admin_booking_client.delete_booking.side_effect = lambda booking_id: _record_deletion(
        deletion_order,
        f"booking:{booking_id}",
    )
    admin_message_client = Mock(spec=MessageClient)
    admin_message_client.delete_message.side_effect = lambda message_id: _record_deletion(
        deletion_order,
        f"message:{message_id}",
    )
    lifecycle = _lifecycle(
        admin_room_client=admin_room_client,
        admin_booking_client=admin_booking_client,
        admin_message_client=admin_message_client,
    )
    lifecycle.track_room(room_name="api-room", room_id=10)
    lifecycle.track_booking(
        room_id=10,
        first_name="Api",
        last_name="Guest",
        booking_id=20,
    )
    lifecycle.track_message(subject="API message", message_id=30)

    lifecycle.cleanup()

    assert deletion_order == ["message:30", "booking:20", "room:10"]


def test_cleanup_accepts_failed_delete_when_resource_is_already_absent() -> None:
    room_client = Mock(spec=RoomClient)
    room_client.get_rooms.return_value = _json_response(200, {"rooms": []})
    admin_room_client = Mock(spec=RoomClient)
    admin_room_client.delete_room.return_value = _json_response(500, {})
    lifecycle = _lifecycle(
        room_client=room_client,
        admin_room_client=admin_room_client,
    )
    lifecycle.track_room(room_name="api-reset-room", room_id=42)

    lifecycle.cleanup()

    admin_room_client.delete_room.assert_called_once_with(42)


def test_cleanup_reports_failure_after_attempting_remaining_resources() -> None:
    room_client = Mock(spec=RoomClient)
    room_client.get_rooms.return_value = _json_response(
        200,
        {"rooms": [{"roomid": 10, "roomName": "api-room"}]},
    )
    admin_room_client = Mock(spec=RoomClient)
    admin_room_client.delete_room.return_value = _json_response(202, {})
    admin_message_client = Mock(spec=MessageClient)
    admin_message_client.delete_message.return_value = _json_response(500, {})
    admin_message_client.get_messages.return_value = _json_response(
        200,
        {"messages": [{"id": 30, "subject": "API message"}]},
    )
    lifecycle = _lifecycle(
        room_client=room_client,
        admin_room_client=admin_room_client,
        admin_message_client=admin_message_client,
    )
    lifecycle.track_room(room_name="api-room", room_id=10)
    lifecycle.track_message(subject="API message", message_id=30)

    with pytest.raises(ResourceCleanupError, match="message 30"):
        lifecycle.cleanup()

    admin_room_client.delete_room.assert_called_once_with(10)


def _lifecycle(
    *,
    room_client: Mock | None = None,
    admin_room_client: Mock | None = None,
    admin_booking_client: Mock | None = None,
    admin_message_client: Mock | None = None,
) -> ApiResourceLifecycle:
    return ApiResourceLifecycle(
        room_client=cast(RoomClient, room_client or Mock(spec=RoomClient)),
        admin_room_client=cast(RoomClient, admin_room_client or Mock(spec=RoomClient)),
        admin_booking_client=cast(
            BookingClient,
            admin_booking_client or Mock(spec=BookingClient),
        ),
        admin_message_client=cast(
            MessageClient,
            admin_message_client or Mock(spec=MessageClient),
        ),
    )


def _record_deletion(order: list[str], resource: str) -> Response:
    order.append(resource)
    return _json_response(202, {})


def _json_response(status_code: int, payload: object) -> Response:
    response = Response()
    response.status_code = status_code
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(payload).encode()
    return response
