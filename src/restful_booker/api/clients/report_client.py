"""Report service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient


class ReportClient(BaseApiClient):
    """Room availability and authenticated booking report operations."""

    def get_room_report(self, room_id: int) -> Response:
        """Return public unavailable periods for one room."""

        return self._request("GET", f"/report/room/{room_id}")

    def get_full_report(self) -> Response:
        """Return the authenticated report for every room."""

        return self._request("GET", "/report")
