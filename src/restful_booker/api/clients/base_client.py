"""Shared HTTP transport without test assertions."""

import logging
from collections.abc import Mapping
from time import perf_counter

from requests import RequestException, Response, Session

from restful_booker.api.exceptions import ApiTransportError
from restful_booker.api.http_logging import request_log_fields, response_log_fields
from restful_booker.api.types import JsonValue, QueryValue

LOGGER = logging.getLogger("restful_booker.api.http")


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

        url = f"{self._api_url}/{path.lstrip('/')}"
        rendered_params, rendered_headers, rendered_cookies, rendered_body = request_log_fields(
            self._session,
            params=params,
            payload=payload,
        )
        LOGGER.info(
            "HTTP request | method=%s | url=%s | params=%s | headers=%s | cookies=%s | body=%s",
            method,
            url,
            rendered_params,
            rendered_headers,
            rendered_cookies,
            rendered_body,
        )

        started_at = perf_counter()
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=None if params is None else dict(params),
                json=None if payload is None else dict(payload),
                timeout=self._timeout_s,
            )
        except RequestException as error:
            elapsed_ms = (perf_counter() - started_at) * 1_000
            LOGGER.error(
                "HTTP failure | method=%s | url=%s | elapsed_ms=%.1f | error=%s: %s",
                method,
                url,
                elapsed_ms,
                type(error).__name__,
                error,
            )
            raise ApiTransportError(
                f"{method.upper()} {url} failed after {elapsed_ms:.1f} ms: "
                f"{type(error).__name__}: {error}"
            ) from None

        elapsed_ms = (perf_counter() - started_at) * 1_000
        response_headers, response_body = response_log_fields(response)
        LOGGER.info(
            "HTTP response | method=%s | url=%s | status=%s | elapsed_ms=%.1f "
            "| headers=%s | body=%s",
            method,
            response.url,
            response.status_code,
            elapsed_ms,
            response_headers,
            response_body,
        )
        return response
