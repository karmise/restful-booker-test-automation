"""Message API contracts."""

from __future__ import annotations

from dataclasses import dataclass

from restful_booker.api.dto._parsing import (
    as_array,
    as_object,
    required_bool,
    required_int,
    required_str,
)
from restful_booker.api.types import JsonValue


@dataclass(frozen=True, slots=True)
class MessageRequest:
    """Contact message creation payload."""

    name: str
    email: str
    phone: str
    subject: str
    description: str

    def to_payload(self) -> dict[str, JsonValue]:
        """Serialize a message using the external API field names."""

        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "subject": self.subject,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class MessageSummary:
    """Message summary returned by the administration list."""

    message_id: int
    name: str
    is_read: bool
    subject: str

    @classmethod
    def from_payload(cls, payload: object) -> MessageSummary:
        """Parse a message summary."""

        data = as_object(payload, context="Message summary")
        return cls(
            message_id=required_int(data, "id"),
            name=required_str(data, "name"),
            is_read=required_bool(data, "read"),
            subject=required_str(data, "subject"),
        )


@dataclass(frozen=True, slots=True)
class MessageCollection:
    """Collection returned by the message list endpoint."""

    messages: tuple[MessageSummary, ...]

    @classmethod
    def from_payload(cls, payload: object) -> MessageCollection:
        """Parse a message collection response."""

        data = as_object(payload, context="Message collection response")
        messages = as_array(data.get("messages"), context="'messages'")
        return cls(messages=tuple(MessageSummary.from_payload(message) for message in messages))

    def find_by_subject(self, subject: str) -> MessageSummary:
        """Find a message created with a unique test subject."""

        matches = [message for message in self.messages if message.subject == subject]
        if len(matches) != 1:
            raise LookupError(
                f"Expected one message with subject '{subject}', found {len(matches)}"
            )
        return matches[0]
