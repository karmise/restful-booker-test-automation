"""HTTP and JSON Schema assertions shared by API services."""

from __future__ import annotations

import json
from http import HTTPStatus
from typing import cast

from requests import Response

from restful_booker.api.schema_registry import SchemaRegistry
from restful_booker.api.types import JsonValue


class ApiAssertions:
    """Generic protocol checks with response diagnostics."""

    def __init__(self, schema_registry: SchemaRegistry) -> None:
        self._schema_registry = schema_registry

    def has_status(
        self,
        response: Response,
        expected: HTTPStatus,
        *,
        because: str,
    ) -> None:
        """Verify an HTTP status with method, URL, and body on failure."""

        assert response.status_code == expected, (
            f"{because}\n"
            f"Expected: {expected.value} {expected.phrase}\n"
            f"Actual: {response.status_code} {response.reason}\n"
            f"Request: {response.request.method} {response.url}\n"
            f"Response body: {response.text}"
        )

    def matches_schema(self, response: Response, schema_name: str) -> None:
        """Verify a successful JSON response against a named contract."""

        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Schema '{schema_name}' requires a JSON response, "
            f"but Content-Type was '{content_type}' for {response.url}"
        )
        self._schema_registry.validate(_response_json(response), schema_name)

    def contains_error(self, response: Response, expected_text: str) -> None:
        """Verify a user-facing error across the platform's error envelope variants."""

        rendered = json.dumps(
            _response_json(response),
            ensure_ascii=False,
            sort_keys=True,
        )
        assert expected_text.lower() in rendered.lower(), (
            f"Expected API error to contain '{expected_text}', but response was: {rendered}"
        )

    def success_flag_is_true(self, response: Response) -> None:
        """Verify the proxy's successful mutation envelope."""

        payload = _response_json(response)
        assert isinstance(payload, dict), (
            f"Mutation response must be a JSON object, got {type(payload).__name__}"
        )
        assert payload.get("success") is True, (
            f"Expected mutation response {{'success': true}}, got {payload}"
        )


def response_json(response: Response) -> JsonValue:
    """Expose response JSON to typed fixtures and domain assertions."""

    return _response_json(response)


def _response_json(response: Response) -> JsonValue:
    try:
        return cast(JsonValue, response.json())
    except ValueError as error:
        raise AssertionError(
            f"Expected JSON from {response.request.method} {response.url}, "
            f"but received: {response.text}"
        ) from error
