"""UI model and test-data fixtures."""

import pytest

from restful_booker.core import Settings
from restful_booker.models import BookingRequest, ContactMessage, Credentials, Room
from restful_booker.testdata import TestDataFactory


@pytest.fixture(scope="session")
def test_data_factory() -> TestDataFactory:
    """Provide the single entry point for generated UI test data."""

    return TestDataFactory()


@pytest.fixture
def contact_message(test_data_factory: TestDataFactory) -> ContactMessage:
    """Create a unique valid contact message."""

    return test_data_factory.contact_message()


@pytest.fixture
def booking_request(test_data_factory: TestDataFactory) -> BookingRequest:
    """Create a valid future reservation request."""

    return test_data_factory.booking_request()


@pytest.fixture(scope="session")
def admin_credentials(settings: Settings) -> Credentials:
    """Expose configured public sandbox credentials as a typed model."""

    return Credentials(
        username=settings.admin_username,
        password=settings.admin_password,
    )


@pytest.fixture(scope="session")
def invalid_admin_credentials() -> Credentials:
    """Provide credentials that cannot authenticate."""

    return Credentials(
        username="invalid-portfolio-user",
        password="invalid-password",
    )


@pytest.fixture(scope="session")
def double_room() -> Room:
    """Describe the stable seeded double room used by UI scenarios."""

    return Room(
        room_id=2,
        name="Double",
        nightly_rate=150,
        features=("TV", "Radio", "Safe"),
    )
