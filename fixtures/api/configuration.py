"""API runtime configuration fixtures."""

import pytest

from restful_booker.core import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Load environment-backed settings once for the API suite."""

    return Settings.from_env()
