"""API-backed resource fixtures used as UI test preconditions."""

import pytest

from fixtures.api.resources import CreatedRoom
from restful_booker.api.resource_lifecycle import ApiResourceLifecycle
from restful_booker.models import ContactMessage, Room


@pytest.fixture
def isolated_room(created_room: CreatedRoom) -> Room:
    """Expose a uniquely created API room through the UI domain model."""

    return Room(
        room_id=created_room.room.room_id,
        name=created_room.room.room_name,
        nightly_rate=created_room.room.room_price,
        features=created_room.room.features,
    )


@pytest.fixture
def contact_message(
    contact_message_data: ContactMessage,
    api_resource_lifecycle: ApiResourceLifecycle,
) -> ContactMessage:
    """Register UI-created contact data for API cleanup after submission."""

    api_resource_lifecycle.track_message(subject=contact_message_data.subject)
    return contact_message_data
