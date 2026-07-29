"""API assertion object fixtures."""

import pytest

from restful_booker.api.assertions import (
    ApiAssertions,
    AuthAssertions,
    BookingAssertions,
    BrandingAssertions,
    MessageAssertions,
    ReportAssertions,
    RoomAssertions,
)
from restful_booker.api.schema_registry import SchemaRegistry


@pytest.fixture(scope="session")
def schema_registry() -> SchemaRegistry:
    return SchemaRegistry()


@pytest.fixture
def api_assertions(schema_registry: SchemaRegistry) -> ApiAssertions:
    return ApiAssertions(schema_registry)


@pytest.fixture
def auth_assertions() -> AuthAssertions:
    return AuthAssertions()


@pytest.fixture
def room_assertions() -> RoomAssertions:
    return RoomAssertions()


@pytest.fixture
def booking_assertions() -> BookingAssertions:
    return BookingAssertions()


@pytest.fixture
def message_assertions() -> MessageAssertions:
    return MessageAssertions()


@pytest.fixture
def branding_assertions() -> BrandingAssertions:
    return BrandingAssertions()


@pytest.fixture
def report_assertions() -> ReportAssertions:
    return ReportAssertions()
