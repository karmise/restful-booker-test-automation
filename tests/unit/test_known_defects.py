"""Status assertions distinguish known defects from unrelated failures."""

from http import HTTPStatus

import allure
import pytest
from requests import Request, Response

from restful_booker.api.assertions import ApiAssertions
from restful_booker.api.exceptions import KnownSandboxDefectError
from restful_booker.api.schema_registry import SchemaRegistry

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Expected failures"),
    allure.epic("Test framework"),
    allure.feature("Expected failures"),
]


@pytest.fixture
def status_assertions() -> ApiAssertions:
    return ApiAssertions(SchemaRegistry())


def test_corrected_not_found_response_passes(status_assertions: ApiAssertions) -> None:
    response = _response(404)

    status_assertions.has_status(
        response,
        HTTPStatus.NOT_FOUND,
        because="Unknown resources should return 404",
        known_defect_status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def test_documented_server_error_raises_known_defect(status_assertions: ApiAssertions) -> None:
    response = _response(500)

    with pytest.raises(KnownSandboxDefectError, match="Known defect: received 500"):
        status_assertions.has_status(
            response,
            HTTPStatus.NOT_FOUND,
            because="Unknown resources should return 404",
            known_defect_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@pytest.mark.parametrize("status", [400, 401, 403, 502])
def test_unrelated_status_remains_an_unexpected_failure(
    status_assertions: ApiAssertions, status: int
) -> None:
    response = _response(status)

    with pytest.raises(AssertionError) as caught:
        status_assertions.has_status(
            response,
            HTTPStatus.NOT_FOUND,
            because="Unknown resources should return 404",
            known_defect_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    assert type(caught.value) is AssertionError
    assert f"Actual: {status}" in str(caught.value)


def test_server_error_requires_explicit_known_defect_declaration(
    status_assertions: ApiAssertions,
) -> None:
    response = _response(500)

    with pytest.raises(AssertionError) as caught:
        status_assertions.has_status(
            response, HTTPStatus.NOT_FOUND, because="Unknown resources should return 404"
        )

    assert type(caught.value) is AssertionError
    assert "Actual: 500" in str(caught.value)


def test_expected_status_is_never_classified_as_known_defect(
    status_assertions: ApiAssertions,
) -> None:
    response = _response(500)

    status_assertions.has_status(
        response,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        because="This scenario deliberately expects a server error",
        known_defect_status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def _response(status: int) -> Response:
    response = Response()
    response.status_code = status
    response._content = b"{}"
    response.url = "https://example.test/api/resource/42"
    response.request = Request("GET", response.url).prepare()
    return response
