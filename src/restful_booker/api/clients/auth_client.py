"""Authentication service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.api.dto import AuthRequest


class AuthClient(BaseApiClient):
    """Authentication operations exposed through the public API proxy."""

    def login(self, credentials: AuthRequest) -> Response:
        """Exchange credentials for a token."""

        return self._request(
            "POST",
            "/auth/login",
            payload=credentials.to_payload(),
        )

    def validate(self, token: str) -> Response:
        """Check whether a token is accepted by the authentication service."""

        return self._request(
            "POST",
            "/auth/validate",
            payload={"token": token},
        )
