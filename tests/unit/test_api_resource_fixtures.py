"""Unit tests for API resource discovery fixtures."""

import json
from typing import cast
from unittest.mock import Mock

import allure
import pytest
from requests import Response

from fixtures.api.resources import wait_for_message
from restful_booker.api.clients import MessageClient

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("API resource fixtures"),
    allure.epic("Test framework"),
    allure.feature("Test-data setup"),
]


def test_message_discovery_retries_until_created_message_is_visible() -> None:
    client = Mock(spec=MessageClient)
    client.get_messages.side_effect = [
        _messages_response([]),
        _messages_response([{"id": 42, "name": "API Guest", "read": False, "subject": "unique"}]),
    ]

    discovered = wait_for_message(
        cast(MessageClient, client),
        subject="unique",
        poll_interval_seconds=0,
    )

    assert discovered.message.message_id == 42
    assert client.get_messages.call_count == 2


def test_message_discovery_reports_a_bounded_timeout() -> None:
    client = Mock(spec=MessageClient)
    client.get_messages.return_value = _messages_response([])

    with pytest.raises(LookupError, match="did not appear within 0 seconds"):
        wait_for_message(
            cast(MessageClient, client),
            subject="missing",
            timeout_seconds=0,
            poll_interval_seconds=0,
        )


def _messages_response(messages: list[dict[str, object]]) -> Response:
    response = Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps({"messages": messages}).encode()
    return response
