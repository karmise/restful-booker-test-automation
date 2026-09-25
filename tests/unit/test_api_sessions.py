"""HTTP fixture isolation and cleanup without contacting the sandbox."""

from contextlib import contextmanager
from unittest.mock import Mock

import allure
import pytest
from requests import Response, Session

from fixtures.api.clients import authenticated_session
from restful_booker.core import Settings

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Session isolation"),
    allure.epic("Test framework"),
    allure.feature("Session isolation"),
]


def test_admin_sessions_do_not_share_cookies_or_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Response()
    response.status_code = 200
    response._content = b'{"token":"issued-token"}'
    request = Mock(return_value=response)
    close = Mock()
    monkeypatch.setattr(Session, "request", request)
    monkeypatch.setattr(Session, "close", close)
    session_context = contextmanager(authenticated_session.__wrapped__)

    with session_context(Settings.from_env()) as first:
        first.cookies.set("foreign", "previous-test")
        first.headers["X-Test-State"] = "previous-test"

    with session_context(Settings.from_env()) as second:
        assert second is not first
        assert second.cookies.get("token") == "issued-token"
        assert "foreign" not in second.cookies
        assert "X-Test-State" not in second.headers

    assert request.call_count == 2
    assert close.call_count == 2


def test_admin_session_closes_when_login_response_cannot_be_parsed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Response()
    response.status_code = 200
    response._content = b'{"token":123}'
    close = Mock()
    monkeypatch.setattr(Session, "request", Mock(return_value=response))
    monkeypatch.setattr(Session, "close", close)
    session_context = contextmanager(authenticated_session.__wrapped__)

    with pytest.raises(TypeError, match="token"), session_context(Settings.from_env()):
        pytest.fail("An invalid token must prevent fixture setup")

    close.assert_called_once()
