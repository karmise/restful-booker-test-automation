"""Room API contracts."""

from __future__ import annotations

from dataclasses import dataclass

from restful_booker.api.dto._parsing import (
    as_array,
    as_object,
    required_bool,
    required_int,
    required_str,
    required_str_tuple,
)
from restful_booker.api.types import JsonValue


@dataclass(frozen=True, slots=True)
class RoomRequest:
    """Room data accepted by the administration API."""

    room_name: str
    room_type: str
    accessible: bool
    image: str
    description: str
    features: tuple[str, ...]
    room_price: int

    def to_payload(self) -> dict[str, JsonValue]:
        """Serialize the room using the external API field names."""

        return {
            "roomName": self.room_name,
            "type": self.room_type,
            "accessible": self.accessible,
            "image": self.image,
            "description": self.description,
            "features": list(self.features),
            "roomPrice": self.room_price,
        }


@dataclass(frozen=True, slots=True)
class RoomResponse:
    """Room returned by the external API."""

    room_id: int
    room_name: str
    room_type: str
    accessible: bool
    image: str
    description: str
    features: tuple[str, ...]
    room_price: int

    @classmethod
    def from_payload(cls, payload: object) -> RoomResponse:
        """Parse a room response."""

        data = as_object(payload, context="Room")
        return cls(
            room_id=required_int(data, "roomid"),
            room_name=required_str(data, "roomName"),
            room_type=required_str(data, "type"),
            accessible=required_bool(data, "accessible"),
            image=required_str(data, "image"),
            description=required_str(data, "description"),
            features=required_str_tuple(data, "features"),
            room_price=required_int(data, "roomPrice"),
        )


@dataclass(frozen=True, slots=True)
class RoomCollection:
    """Collection returned by the room search endpoint."""

    rooms: tuple[RoomResponse, ...]

    @classmethod
    def from_payload(cls, payload: object) -> RoomCollection:
        """Parse a room collection response."""

        data = as_object(payload, context="Room collection response")
        rooms = as_array(data.get("rooms"), context="'rooms'")
        return cls(rooms=tuple(RoomResponse.from_payload(room) for room in rooms))

    def find_by_name(self, room_name: str) -> RoomResponse:
        """Find the uniquely named room created by a test."""

        matches = [room for room in self.rooms if room.room_name == room_name]
        if len(matches) != 1:
            raise LookupError(f"Expected one room named '{room_name}', found {len(matches)}")
        return matches[0]
