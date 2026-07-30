"""Typed API request-data fixtures."""

import pytest

from restful_booker.api.dto import AuthRequest, MessageRequest, RoomRequest
from restful_booker.api.testdata import ApiTestDataFactory
from restful_booker.core import Settings

_MISSING_RESOURCE_ID = 2_000_000_000


@pytest.fixture(scope="session")
def api_test_data_factory() -> ApiTestDataFactory:
    return ApiTestDataFactory()


@pytest.fixture
def valid_api_credentials(
    api_test_data_factory: ApiTestDataFactory,
    settings: Settings,
) -> AuthRequest:
    return api_test_data_factory.auth_request(
        username=settings.admin_username,
        password=settings.admin_password,
    )


@pytest.fixture
def invalid_api_credentials(
    api_test_data_factory: ApiTestDataFactory,
) -> AuthRequest:
    return api_test_data_factory.auth_request(
        username="invalid-api-user",
        password="invalid-api-password",
    )


@pytest.fixture
def unknown_authentication_token(
    api_test_data_factory: ApiTestDataFactory,
) -> str:
    return api_test_data_factory.unknown_authentication_token()


@pytest.fixture
def room_request(api_test_data_factory: ApiTestDataFactory) -> RoomRequest:
    return api_test_data_factory.room_request()


@pytest.fixture
def invalid_message_request(
    api_test_data_factory: ApiTestDataFactory,
) -> MessageRequest:
    return api_test_data_factory.message_with_invalid_email()


@pytest.fixture(scope="session")
def missing_resource_id() -> int:
    """Provide a valid integer identifier outside the sandbox's generated range."""

    return _MISSING_RESOURCE_ID
