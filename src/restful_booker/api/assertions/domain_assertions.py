"""Business assertions for API DTOs and service-specific outcomes."""

from __future__ import annotations

from restful_booker.api.dto import (
    BookingRequest,
    BookingResponse,
    MessageRequest,
    MessageSummary,
    RoomRequest,
    RoomResponse,
    TokenResponse,
)


class AuthAssertions:
    """Authentication-domain checks."""

    def token_was_issued(self, token: TokenResponse) -> None:
        """Verify the public token contract."""

        assert len(token.token) >= 16, (
            f"Authentication token should contain at least 16 characters, got {len(token.token)}"
        )

    def token_is_valid(self, payload: object) -> None:
        """Verify token validation response semantics."""

        assert payload == {"valid": True}, (
            f"Valid authentication token should return {{'valid': true}}, got {payload}"
        )


class RoomAssertions:
    """Room-domain checks."""

    def created_room_matches(
        self,
        actual: RoomResponse,
        expected: RoomRequest,
    ) -> None:
        """Verify that room discovery returns all submitted values."""

        assert actual.room_name == expected.room_name, (
            f"Created room name should be '{expected.room_name}', got '{actual.room_name}'"
        )
        assert actual.room_type == expected.room_type, (
            f"Created room type should be '{expected.room_type}', got '{actual.room_type}'"
        )
        assert actual.accessible is expected.accessible, (
            f"Created room accessibility should be {expected.accessible}, got {actual.accessible}"
        )
        assert actual.image == expected.image, (
            f"Created room image should be '{expected.image}', got '{actual.image}'"
        )
        assert actual.description == expected.description, (
            "Created room description does not match the submitted description"
        )
        assert actual.features == expected.features, (
            f"Created room features should be {expected.features}, got {actual.features}"
        )
        assert actual.room_price == expected.room_price, (
            f"Created room price should be {expected.room_price}, got {actual.room_price}"
        )


class BookingAssertions:
    """Booking-domain checks."""

    def created_booking_matches(
        self,
        actual: BookingResponse,
        expected: BookingRequest,
    ) -> None:
        """Verify that an authenticated search returns the submitted booking."""

        assert actual.room_id == expected.room_id, (
            f"Created booking should belong to room {expected.room_id}, got room {actual.room_id}"
        )
        assert actual.first_name == expected.first_name, (
            f"Created booking first name should be '{expected.first_name}', "
            f"got '{actual.first_name}'"
        )
        assert actual.last_name == expected.last_name, (
            f"Created booking last name should be '{expected.last_name}', got '{actual.last_name}'"
        )
        assert actual.deposit_paid is expected.deposit_paid, (
            f"Created booking deposit flag should be {expected.deposit_paid}, "
            f"got {actual.deposit_paid}"
        )
        assert actual.dates == expected.dates, (
            f"Created booking dates should be {expected.dates}, got {actual.dates}"
        )


class MessageAssertions:
    """Message-domain checks."""

    def created_message_matches(
        self,
        actual: MessageSummary,
        expected: MessageRequest,
    ) -> None:
        """Verify that a created contact message appears in administration."""

        assert actual.name == expected.name, (
            f"Created message sender should be '{expected.name}', got '{actual.name}'"
        )
        assert actual.subject == expected.subject, (
            f"Created message subject should be '{expected.subject}', got '{actual.subject}'"
        )
        assert actual.is_read is False, "A newly created contact message should be unread"


class BrandingAssertions:
    """Branding-domain checks."""

    def identifies_property(self, payload: object) -> None:
        """Verify that branding contains the property and contact identity."""

        assert isinstance(payload, dict), "Branding response must be a JSON object"
        assert payload.get("name") == "Shady Meadows B&B", (
            "Branding should identify the property as 'Shady Meadows B&B'"
        )
        contact = payload.get("contact")
        assert isinstance(contact, dict), "Branding contact must be a JSON object"
        assert contact.get("email"), "Branding contact email must not be empty"


class ReportAssertions:
    """Report-domain checks."""

    def has_no_entries_for_new_room(self, payload: object) -> None:
        """Verify that a newly created room starts without unavailable periods."""

        assert payload == {"report": []}, (
            f"A newly created room should have an empty report, got {payload}"
        )
