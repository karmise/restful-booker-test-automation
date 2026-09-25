"""Transport behavior remains independent of application status assertions."""

from typing import cast
from unittest.mock import Mock

import allure
import pytest
from requests import Response, Session, Timeout

from restful_booker.api.clients import RoomClient
from restful_booker.api.exceptions import ApiTransportError

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("HTTP transport"),
    allure.epic("Test framework"),
    allure.feature("HTTP transport"),
]


@pytest.mark.parametrize("status", [200, 401, 404, 500])
def test_transport_returns_raw_responses_and_explicit_timeouts(status: int) -> None:
    session = Mock(spec=Session)
    session.headers = {}
    session.cookies = []
    response = Response()
    response.status_code = status
    response._content = b"{}"
    session.request.return_value = response
    client = RoomClient(cast(Session, session), base_url="https://example.test/", timeout_s=(2, 7))

    assert client.get_room(42) is response
    session.request.assert_called_once_with(
        method="GET", url="https://example.test/api/room/42", params=None, json=None, timeout=(2, 7)
    )


def test_transport_reports_timeouts_without_retrying() -> None:
    session = Mock(spec=Session)
    session.headers = {}
    session.cookies = []
    session.request.side_effect = Timeout("Read timed out")
    client = RoomClient(cast(Session, session), base_url="https://example.test", timeout_s=(2, 7))

    with pytest.raises(ApiTransportError, match="Timeout"):
        client.get_room(42)

    assert session.request.call_count == 1
