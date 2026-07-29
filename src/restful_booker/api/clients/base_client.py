"""Shared HTTP transport without test assertions."""

from collections.abc import Mapping

from requests import Response, Session

from restful_booker.api.types import JsonValue, QueryValue


class BaseApiClient:
    """Own URL construction, session reuse, and request timeout."""

    def __init__(
        self,
        session: Session,
        *,
        base_url: str,
        timeout_s: int,
    ) -> None:
        self._session = session
        self._api_url = f"{base_url.rstrip('/')}/api"
        self._timeout_s = timeout_s

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, QueryValue] | None = None,
        payload: Mapping[str, JsonValue] | None = None,
    ) -> Response:
        """Send a request and return the raw response for the assertion layer."""

        return self._session.request(
            method=method,
            url=f"{self._api_url}/{path.lstrip('/')}",
            params=None if params is None else dict(params),
            json=None if payload is None else dict(payload),
            timeout=self._timeout_s,
        )
