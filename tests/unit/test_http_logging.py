"""Unit tests for safe HTTP diagnostic rendering."""

import json

import allure
import pytest
from requests import Response, Session

from restful_booker.api.http_logging import (
    MAX_BODY_CHARACTERS,
    REDACTED,
    request_log_fields,
    response_log_fields,
)

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("HTTP diagnostics"),
    allure.epic("Test framework"),
    allure.feature("Safe HTTP logging"),
]

_JSON_CONTENT_TYPE = "application/json"
_TEXT_CONTENT_TYPE = "text/plain"
_TRUNCATION_OVERFLOW = 12


def test_request_log_fields_redact_credentials_headers_and_cookies() -> None:
    session = Session()
    session.headers.update({"Authorization": "Bearer secret", "X-Trace": "trace-1"})
    session.cookies.set("token", "cookie-secret")

    params, headers, cookies, body = request_log_fields(
        session,
        params={"page": 2, "token": "query-secret"},
        payload={
            "username": "admin",
            "password": "body-secret",
            "profile": {"secret": "nested-secret", "displayName": "Test User"},
        },
    )

    assert json.loads(params) == {"page": 2, "token": REDACTED}
    assert json.loads(headers)["Authorization"] == REDACTED
    assert json.loads(headers)["X-Trace"] == "trace-1"
    assert json.loads(cookies) == {"token": REDACTED}
    assert json.loads(body) == {
        "password": REDACTED,
        "profile": {"displayName": "Test User", "secret": REDACTED},
        "username": "admin",
    }


def test_response_log_fields_redact_nested_json_and_sensitive_headers() -> None:
    response = _response(
        b'{"user":{"token":"secret","name":"Test"},"items":[{"password":"hidden"}]}',
        content_type=_JSON_CONTENT_TYPE,
        headers={"Set-Cookie": "token=secret", "X-Trace": "trace-2"},
    )

    headers, body = response_log_fields(response)

    assert json.loads(headers) == {
        "Content-Type": _JSON_CONTENT_TYPE,
        "Set-Cookie": REDACTED,
        "X-Trace": "trace-2",
    }
    assert json.loads(body) == {
        "items": [{"password": REDACTED}],
        "user": {"name": "Test", "token": REDACTED},
    }


def test_response_log_fields_fall_back_to_text_for_invalid_json() -> None:
    response = _response(
        b"upstream returned invalid JSON",
        content_type=_JSON_CONTENT_TYPE,
    )

    _, body = response_log_fields(response)

    assert body == "upstream returned invalid JSON"


def test_response_log_fields_truncate_large_text_body() -> None:
    response = _response(
        b"x" * (MAX_BODY_CHARACTERS + _TRUNCATION_OVERFLOW),
        content_type=_TEXT_CONTENT_TYPE,
    )

    _, body = response_log_fields(response)

    assert body == (f"{'x' * MAX_BODY_CHARACTERS}... <truncated {_TRUNCATION_OVERFLOW} characters>")


def _response(
    content: bytes,
    *,
    content_type: str,
    headers: dict[str, str] | None = None,
) -> Response:
    response = Response()
    response.status_code = 200
    response._content = content
    response.headers.update(headers or {})
    response.headers["Content-Type"] = content_type
    response.encoding = "utf-8"
    return response
