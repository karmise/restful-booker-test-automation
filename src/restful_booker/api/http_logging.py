"""Safe, compact HTTP diagnostics for local API test debugging."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

from requests import Response, Session

from restful_booker.api.types import JsonValue, QueryValue

REDACTED = "<redacted>"
MAX_BODY_CHARACTERS = 4_000

_SENSITIVE_FIELDS = frozenset(
    {
        "access_token",
        "authorization",
        "cookie",
        "password",
        "proxy-authorization",
        "refresh_token",
        "secret",
        "set-cookie",
        "token",
        "x-api-key",
    }
)


def request_log_fields(
    session: Session,
    *,
    params: Mapping[str, QueryValue] | None,
    payload: Mapping[str, JsonValue] | None,
) -> tuple[str, str, str, str]:
    """Render request metadata without exposing authentication material."""

    headers = dict(session.headers)
    if payload is not None:
        headers.setdefault("Content-Type", "application/json")
    cookies: dict[str, JsonValue] = {cookie.name: REDACTED for cookie in session.cookies}
    return (
        _render_json(_redact_mapping(params or {})),
        _render_json(_redact_mapping(headers)),
        _render_json(cookies),
        _render_json(_redact_mapping(payload or {})),
    )


def response_log_fields(response: Response) -> tuple[str, str]:
    """Render response headers and body with secrets masked."""

    headers = _render_json(_redact_mapping(dict(response.headers)))
    return headers, _render_body(response)


def _render_body(response: Response) -> str:
    if not response.content:
        return "<empty>"

    content_type = response.headers.get("Content-Type", "")
    if "json" in content_type.lower():
        try:
            payload = cast(JsonValue, response.json())
        except ValueError:
            return _truncate(response.text)
        return _render_json(_redact_json(payload))
    return _truncate(response.text)


def _redact_json(value: JsonValue) -> JsonValue:
    if isinstance(value, dict):
        return _redact_mapping(value)
    if isinstance(value, list):
        return [_redact_json(item) for item in value]
    return value


def _redact_mapping(
    values: Mapping[str, JsonValue] | Mapping[str, QueryValue] | Mapping[str, str],
) -> dict[str, JsonValue]:
    return {
        key: REDACTED if key.lower() in _SENSITIVE_FIELDS else _redact_value(value)
        for key, value in values.items()
    }


def _redact_value(value: object) -> JsonValue:
    if isinstance(value, dict):
        return _redact_mapping(cast(dict[str, JsonValue], value))
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _render_json(value: JsonValue) -> str:
    return _truncate(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _truncate(value: str) -> str:
    if len(value) <= MAX_BODY_CHARACTERS:
        return value
    omitted = len(value) - MAX_BODY_CHARACTERS
    return f"{value[:MAX_BODY_CHARACTERS]}... <truncated {omitted} characters>"
