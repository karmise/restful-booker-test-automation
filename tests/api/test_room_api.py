"""Room API scenarios."""

from http import HTTPStatus

import allure
import pytest

from restful_booker.api.assertions import ApiAssertions, RoomAssertions
from restful_booker.api.clients import RoomClient
from restful_booker.api.dto import RoomRequest
from tests.api.fixtures.resources import CreatedRoom

pytestmark = [
    allure.epic("REST API"),
    allure.feature("Room service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Room discovery")
@allure.title("Room collection matches the public contract")
@allure.severity(allure.severity_level.CRITICAL)
def test_room_collection_matches_public_contract(
    room_client: RoomClient,
    api_assertions: ApiAssertions,
) -> None:
    with allure.step("Request the public room collection"):
        response = room_client.get_rooms()

    with allure.step("Verify the room collection response contract"):
        api_assertions.has_status(
            response,
            HTTPStatus.OK,
            because="The home page requires public room discovery",
        )
        api_assertions.matches_schema(response, "rooms")


@pytest.mark.api
@pytest.mark.regression
@allure.story("Room administration")
@allure.title("Administrator can create an isolated room")
@allure.severity(allure.severity_level.CRITICAL)
def test_administrator_can_create_isolated_room(
    created_room: CreatedRoom,
    api_assertions: ApiAssertions,
    room_assertions: RoomAssertions,
) -> None:
    with allure.step("Verify that the isolated room was created and is discoverable"):
        api_assertions.has_status(
            created_room.create_response,
            HTTPStatus.OK,
            because="An authenticated administrator should be able to create a room",
        )
        api_assertions.success_flag_is_true(created_room.create_response)
        api_assertions.matches_schema(created_room.collection_response, "rooms")
        room_assertions.created_room_matches(created_room.room, created_room.request)


@pytest.mark.api
@pytest.mark.regression
@allure.story("Room authorization")
@allure.title("Anonymous user cannot create a room")
@allure.severity(allure.severity_level.CRITICAL)
def test_anonymous_user_cannot_create_room(
    room_client: RoomClient,
    api_assertions: ApiAssertions,
    room_request: RoomRequest,
) -> None:
    with allure.step("Attempt to create a room without authentication"):
        response = room_client.create_room(room_request)

    with allure.step("Verify that anonymous room creation is rejected"):
        api_assertions.has_status(
            response,
            HTTPStatus.UNAUTHORIZED,
            because="Room creation is restricted to authenticated administrators",
        )
        api_assertions.contains_error(response, "Authentication required")
