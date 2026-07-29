"""Authentication API contracts."""

from __future__ import annotations

from dataclasses import dataclass

from restful_booker.api.dto._parsing import as_object, required_str
from restful_booker.api.types import JsonValue


@dataclass(frozen=True, slots=True)
class AuthRequest:
    """Credentials submitted to the authentication API."""

    username: str
    password: str

    def to_payload(self) -> dict[str, JsonValue]:
        """Serialize credentials using the external API field names."""

        return {
            "username": self.username,
            "password": self.password,
        }


@dataclass(frozen=True, slots=True)
class TokenResponse:
    """Token returned by a successful external API login."""

    token: str

    @classmethod
    def from_payload(cls, payload: object) -> TokenResponse:
        """Parse a login response."""

        data = as_object(payload, context="Authentication response")
        return cls(token=required_str(data, "token"))
