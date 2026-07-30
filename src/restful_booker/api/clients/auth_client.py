"""Authentication service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.api.dto import AuthRequest
from restful_booker.reporting import report_step


class AuthClient(BaseApiClient):
    """Authentication operations exposed through the public API proxy."""

    @report_step("Authenticate with administrator credentials")
    def login(self, credentials: AuthRequest) -> Response:
        """Exchange credentials for a token."""

        return self._request(
            "POST",
            "/auth/login",
            payload=credentials.to_payload(),
        )

    @report_step("Validate an authentication token")
    def validate(self, token: str) -> Response:
        """Check whether a token is accepted by the authentication service."""

        return self._request(
            "POST",
            "/auth/validate",
            payload={"token": token},
        )
