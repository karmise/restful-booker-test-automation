"""Best-effort cleanup for resources created by tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias

from requests import Response

from restful_booker.api.clients import BookingClient, MessageClient, RoomClient


class ResourceCleanupError(RuntimeError):
    """Report one or more resources that could not be cleaned up safely."""


@dataclass(slots=True)
class _TrackedRoom:
    room_name: str
    room_id: int | None = None


@dataclass(slots=True)
class _TrackedBooking:
    room_id: int
    first_name: str
    last_name: str
    booking_id: int | None = None


@dataclass(slots=True)
class _TrackedMessage:
    subject: str
    message_id: int | None = None


_TrackedResource: TypeAlias = _TrackedRoom | _TrackedBooking | _TrackedMessage


class ApiResourceLifecycle:
    """Track test-owned resources and remove them in reverse creation order."""

    def __init__(
        self,
        *,
        room_client: RoomClient,
        admin_room_client: RoomClient,
        admin_booking_client: BookingClient,
        admin_message_client: MessageClient,
    ) -> None:
        self._room_client = room_client
        self._admin_room_client = admin_room_client
        self._admin_booking_client = admin_booking_client
        self._admin_message_client = admin_message_client
        self._resources: list[_TrackedResource] = []

    def track_room(self, *, room_name: str, room_id: int | None = None) -> None:
        """Register a uniquely named room for later cleanup."""

        existing = self._find_tracked_room(room_name)
        if existing is None:
            self._resources.append(_TrackedRoom(room_name=room_name, room_id=room_id))
        elif room_id is not None:
            existing.room_id = room_id

    def track_booking(
        self,
        *,
        room_id: int,
        first_name: str,
        last_name: str,
        booking_id: int | None = None,
    ) -> None:
        """Register a uniquely identified booking for later cleanup."""

        existing = self._find_tracked_booking(
            room_id=room_id,
            first_name=first_name,
            last_name=last_name,
        )
        if existing is None:
            self._resources.append(
                _TrackedBooking(
                    room_id=room_id,
                    first_name=first_name,
                    last_name=last_name,
                    booking_id=booking_id,
                )
            )
        elif booking_id is not None:
            existing.booking_id = booking_id

    def track_message(self, *, subject: str, message_id: int | None = None) -> None:
        """Register a uniquely titled contact message for later cleanup."""

        existing = self._find_tracked_message(subject)
        if existing is None:
            self._resources.append(_TrackedMessage(subject=subject, message_id=message_id))
        elif message_id is not None:
            existing.message_id = message_id

    def cleanup(self) -> None:
        """Remove tracked resources and report all cleanup failures together."""

        failures: list[str] = []
        while self._resources:
            resource = self._resources.pop()
            try:
                self._cleanup_resource(resource)
            except Exception as error:
                failures.append(f"{self._describe(resource)}: {error}")

        if failures:
            details = "\n".join(f"- {failure}" for failure in failures)
            raise ResourceCleanupError(f"Failed to clean up test resources:\n{details}")

    def _cleanup_resource(self, resource: _TrackedResource) -> None:
        if isinstance(resource, _TrackedBooking):
            self._cleanup_booking(resource)
        elif isinstance(resource, _TrackedMessage):
            self._cleanup_message(resource)
        else:
            self._cleanup_room(resource)

    def _cleanup_room(self, room: _TrackedRoom) -> None:
        room_id = room.room_id or self._find_room_id(room.room_name)
        if room_id is None:
            return

        response = self._admin_room_client.delete_room(room_id)
        if response.status_code == 202:
            return
        if self._find_room_id(room.room_name) is None:
            return
        _raise_delete_error(response, resource=f"room {room_id}")

    def _cleanup_booking(self, booking: _TrackedBooking) -> None:
        booking_id = booking.booking_id or self._find_booking_id(booking)
        if booking_id is None:
            return

        response = self._admin_booking_client.delete_booking(booking_id)
        if response.status_code == 202:
            return
        if self._find_booking_id(booking) is None:
            return
        _raise_delete_error(response, resource=f"booking {booking_id}")

    def _cleanup_message(self, message: _TrackedMessage) -> None:
        message_id = message.message_id or self._find_message_id(message.subject)
        if message_id is None:
            return

        response = self._admin_message_client.delete_message(message_id)
        if response.status_code == 202:
            return
        if self._find_message_id(message.subject) is None:
            return
        _raise_delete_error(response, resource=f"message {message_id}")

    def _find_room_id(self, room_name: str) -> int | None:
        response = self._room_client.get_rooms()
        items = _response_items(response, key="rooms", resource="room discovery")
        return _find_unique_id(
            items,
            id_field="roomid",
            matches=lambda item: item.get("roomName") == room_name,
            identity=f"room named '{room_name}'",
        )

    def _find_booking_id(self, booking: _TrackedBooking) -> int | None:
        response = self._admin_booking_client.get_bookings_for_room(booking.room_id)
        items = _response_items(response, key="bookings", resource="booking discovery")
        return _find_unique_id(
            items,
            id_field="bookingid",
            matches=lambda item: (
                item.get("firstname") == booking.first_name
                and item.get("lastname") == booking.last_name
            ),
            identity=f"booking for '{booking.first_name} {booking.last_name}'",
        )

    def _find_message_id(self, subject: str) -> int | None:
        response = self._admin_message_client.get_messages()
        items = _response_items(response, key="messages", resource="message discovery")
        return _find_unique_id(
            items,
            id_field="id",
            matches=lambda item: item.get("subject") == subject,
            identity=f"message with subject '{subject}'",
        )

    def _find_tracked_room(self, room_name: str) -> _TrackedRoom | None:
        return next(
            (
                resource
                for resource in self._resources
                if isinstance(resource, _TrackedRoom) and resource.room_name == room_name
            ),
            None,
        )

    def _find_tracked_booking(
        self,
        *,
        room_id: int,
        first_name: str,
        last_name: str,
    ) -> _TrackedBooking | None:
        return next(
            (
                resource
                for resource in self._resources
                if isinstance(resource, _TrackedBooking)
                and resource.room_id == room_id
                and resource.first_name == first_name
                and resource.last_name == last_name
            ),
            None,
        )

    def _find_tracked_message(self, subject: str) -> _TrackedMessage | None:
        return next(
            (
                resource
                for resource in self._resources
                if isinstance(resource, _TrackedMessage) and resource.subject == subject
            ),
            None,
        )

    @staticmethod
    def _describe(resource: _TrackedResource) -> str:
        if isinstance(resource, _TrackedRoom):
            return f"room '{resource.room_name}'"
        if isinstance(resource, _TrackedBooking):
            return f"booking for '{resource.first_name} {resource.last_name}'"
        return f"message '{resource.subject}'"


def _response_items(
    response: Response,
    *,
    key: str,
    resource: str,
) -> list[dict[str, object]]:
    if response.status_code != 200:
        raise ResourceCleanupError(
            f"{resource} returned status {response.status_code} instead of 200"
        )

    try:
        payload: object = response.json()
    except ValueError as error:
        raise ResourceCleanupError(f"{resource} returned invalid JSON") from error

    if not isinstance(payload, dict):
        raise ResourceCleanupError(f"{resource} response is not a JSON object")
    raw_items = payload.get(key)
    if not isinstance(raw_items, list):
        raise ResourceCleanupError(f"{resource} response does not contain a '{key}' array")

    if not all(isinstance(item, dict) for item in raw_items):
        raise ResourceCleanupError(f"{resource} '{key}' array contains a non-object item")
    return raw_items


def _find_unique_id(
    items: list[dict[str, object]],
    *,
    id_field: str,
    matches: Callable[[dict[str, object]], bool],
    identity: str,
) -> int | None:
    matching_items = [item for item in items if matches(item)]
    if not matching_items:
        return None
    if len(matching_items) != 1:
        raise ResourceCleanupError(f"Expected at most one {identity}, found {len(matching_items)}")

    resource_id = matching_items[0].get(id_field)
    if type(resource_id) is not int:
        raise ResourceCleanupError(f"{identity} has an invalid '{id_field}' value")
    return resource_id


def _raise_delete_error(response: Response, *, resource: str) -> None:
    raise ResourceCleanupError(
        f"deleting {resource} returned status {response.status_code} instead of 202"
    )
