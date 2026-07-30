"""Message service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.api.dto import MessageRequest
from restful_booker.reporting import report_step


class MessageClient(BaseApiClient):
    """Contact-message creation and administration operations."""

    @report_step("Request contact messages")
    def get_messages(self) -> Response:
        """Return message summaries."""

        return self._request("GET", "/message")

    @report_step("Request a contact message by identifier")
    def get_message(self, message_id: int) -> Response:
        """Return one complete contact message."""

        return self._request("GET", f"/message/{message_id}")

    @report_step("Create a contact message")
    def create_message(self, message: MessageRequest) -> Response:
        """Create a contact message."""

        return self._request(
            "POST",
            "/message",
            payload=message.to_payload(),
        )

    @report_step("Delete a contact message")
    def delete_message(self, message_id: int) -> Response:
        """Delete a message using the current session."""

        return self._request("DELETE", f"/message/{message_id}")

    @report_step("Mark a contact message as read")
    def mark_as_read(self, message_id: int) -> Response:
        """Mark a message as read using the current session."""

        return self._request("PUT", f"/message/{message_id}/read")
