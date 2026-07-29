"""Message service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.api.dto import MessageRequest


class MessageClient(BaseApiClient):
    """Contact-message creation and administration operations."""

    def get_messages(self) -> Response:
        """Return message summaries."""

        return self._request("GET", "/message")

    def create_message(self, message: MessageRequest) -> Response:
        """Create a contact message."""

        return self._request(
            "POST",
            "/message",
            payload=message.to_payload(),
        )

    def delete_message(self, message_id: int) -> Response:
        """Delete a message using the current session."""

        return self._request("DELETE", f"/message/{message_id}")

    def mark_as_read(self, message_id: int) -> Response:
        """Mark a message as read using the current session."""

        return self._request("PUT", f"/message/{message_id}/read")
