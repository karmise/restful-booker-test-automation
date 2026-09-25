"""Known server defects must not absorb authentication or transport failures."""

from collections.abc import Callable
from typing import Any
from unittest.mock import Mock

import allure
import pytest
from requests import Request, Response

from restful_booker.api.assertions import ApiAssertions
from restful_booker.api.exceptions import ApiTransportError
from restful_booker.api.schema_registry import SchemaRegistry
from tests.api.known_defects import KnownSandboxDefectError
from tests.api.test_message_api import (
    test_unknown_message_identifier_returns_not_found as message_case,
)
from tests.api.test_room_api import test_unknown_room_identifier_returns_not_found as room_case

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Expected failures"),
    allure.epic("Test framework"),
    allure.feature("Expected failures"),
]


@pytest.mark.parametrize(
    ("scenario", "method"), [(room_case, "get_room"), (message_case, "get_message")]
)
@pytest.mark.parametrize("status", [401, 404, 500])
def test_only_documented_server_status_is_a_known_defect(
    scenario: Callable[..., Any], method: str, status: int
) -> None:
    response = Response()
    response.status_code = status
    response._content = b"{}"
    response.url = "https://example.test/api/resource/42"
    response.request = Request("GET", response.url).prepare()
    client = Mock()
    getattr(client, method).return_value = response
    assertions = ApiAssertions(SchemaRegistry())

    if status == 404:
        scenario(client, assertions, 42)
    elif status == 500:
        with pytest.raises(KnownSandboxDefectError):
            scenario(client, assertions, 42)
    else:
        with pytest.raises(AssertionError) as caught:
            scenario(client, assertions, 42)
        assert not isinstance(caught.value, KnownSandboxDefectError)


@pytest.mark.parametrize(
    ("scenario", "method"), [(room_case, "get_room"), (message_case, "get_message")]
)
def test_transport_failure_is_not_a_known_sandbox_defect(
    scenario: Callable[..., Any], method: str
) -> None:
    client = Mock()
    getattr(client, method).side_effect = ApiTransportError("Connection failed")

    with pytest.raises(ApiTransportError, match="Connection failed"):
        scenario(client, ApiAssertions(SchemaRegistry()), 42)
