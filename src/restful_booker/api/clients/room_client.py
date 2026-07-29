"""Room service client."""

from datetime import date

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.api.dto import RoomRequest
from restful_booker.api.types import QueryValue


class RoomClient(BaseApiClient):
    """Room discovery and administration operations."""

    def get_rooms(
        self,
        *,
        check_in: date | None = None,
        check_out: date | None = None,
    ) -> Response:
        """Return rooms, optionally filtered by a requested stay."""

        params: dict[str, QueryValue] | None = None
        if check_in is not None and check_out is not None:
            params = {
                "checkin": check_in.isoformat(),
                "checkout": check_out.isoformat(),
            }
        return self._request("GET", "/room", params=params)

    def get_room(self, room_id: int) -> Response:
        """Return a room by identifier."""

        return self._request("GET", f"/room/{room_id}")

    def create_room(self, room: RoomRequest) -> Response:
        """Create a room using the current session."""

        return self._request("POST", "/room", payload=room.to_payload())

    def delete_room(self, room_id: int) -> Response:
        """Delete a room using the current session."""

        return self._request("DELETE", f"/room/{room_id}")
