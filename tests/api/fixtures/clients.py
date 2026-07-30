"""HTTP session and service-client fixtures."""

from collections.abc import Iterator

import allure
import pytest
from requests import Session

from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import (
    AuthClient,
    BookingClient,
    BrandingClient,
    MessageClient,
    ReportClient,
    RoomClient,
)
from restful_booker.api.dto import AuthRequest, TokenResponse
from restful_booker.core import Settings


@pytest.fixture
def public_session() -> Iterator[Session]:
    """Provide a clean unauthenticated HTTP session for each test."""

    with Session() as session:
        session.headers.update({"Accept": "application/json"})
        yield session


@pytest.fixture(scope="session")
@allure.title("Authenticate the API administrator")
def authenticated_session(settings: Settings) -> Iterator[Session]:
    """Authenticate once and reuse the administrator token across API tests."""

    with Session() as session:
        session.headers.update({"Accept": "application/json"})
        auth_client = AuthClient(
            session,
            base_url=settings.base_url,
            timeout_s=settings.api_timeout_s,
        )
        response = auth_client.login(
            AuthRequest(
                username=settings.admin_username,
                password=settings.admin_password,
            )
        )
        if response.status_code != 200:
            raise RuntimeError(
                "API fixture could not authenticate the administrator: "
                f"{response.status_code} {response.text}"
            )

        token = TokenResponse.from_payload(response_json(response)).token
        session.cookies.set("token", token)
        yield session


@pytest.fixture
def auth_client(public_session: Session, settings: Settings) -> AuthClient:
    return AuthClient(
        public_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def room_client(public_session: Session, settings: Settings) -> RoomClient:
    return RoomClient(
        public_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def admin_room_client(
    authenticated_session: Session,
    settings: Settings,
) -> RoomClient:
    return RoomClient(
        authenticated_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def booking_client(
    public_session: Session,
    settings: Settings,
) -> BookingClient:
    return BookingClient(
        public_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def admin_booking_client(
    authenticated_session: Session,
    settings: Settings,
) -> BookingClient:
    return BookingClient(
        authenticated_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def message_client(
    public_session: Session,
    settings: Settings,
) -> MessageClient:
    return MessageClient(
        public_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def admin_message_client(
    authenticated_session: Session,
    settings: Settings,
) -> MessageClient:
    return MessageClient(
        authenticated_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def branding_client(
    public_session: Session,
    settings: Settings,
) -> BrandingClient:
    return BrandingClient(
        public_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )


@pytest.fixture
def report_client(
    public_session: Session,
    settings: Settings,
) -> ReportClient:
    return ReportClient(
        public_session,
        base_url=settings.base_url,
        timeout_s=settings.api_timeout_s,
    )
