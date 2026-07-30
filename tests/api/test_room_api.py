"""Room API scenarios."""

from http import HTTPStatus

import allure
import pytest

from fixtures.api.resources import CreatedBooking, CreatedRoom
from restful_booker.api.assertions import ApiAssertions, RoomAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import RoomClient
from restful_booker.api.dto import RoomCollection, RoomRequest, RoomResponse

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("API tests"),
    allure.sub_suite("Room service"),
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
    response = room_client.get_rooms()

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
    response = room_client.create_room(room_request)

    api_assertions.has_status(
        response,
        HTTPStatus.UNAUTHORIZED,
        because="Room creation is restricted to authenticated administrators",
    )
    api_assertions.contains_error(response, "Authentication required")


@pytest.mark.api
@pytest.mark.regression
@allure.story("Room discovery")
@allure.title("Created room can be retrieved by identifier")
@allure.severity(allure.severity_level.CRITICAL)
def test_created_room_can_be_retrieved_by_identifier(
    room_client: RoomClient,
    api_assertions: ApiAssertions,
    room_assertions: RoomAssertions,
    created_room: CreatedRoom,
) -> None:
    response = room_client.get_room(created_room.room.room_id)

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="A created room should be retrievable from its canonical resource URL",
    )
    room_assertions.created_room_matches(
        RoomResponse.from_payload(response_json(response)),
        created_room.request,
    )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Room authorization")
@allure.title("Anonymous user cannot delete a room")
@allure.severity(allure.severity_level.CRITICAL)
def test_anonymous_user_cannot_delete_room(
    room_client: RoomClient,
    api_assertions: ApiAssertions,
    created_room: CreatedRoom,
) -> None:
    response = room_client.delete_room(created_room.room.room_id)

    api_assertions.has_status(
        response,
        HTTPStatus.FORBIDDEN,
        because="Room deletion must be restricted to authenticated administrators",
    )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Room availability")
@allure.title("Booked room is excluded from matching availability search")
@allure.severity(allure.severity_level.CRITICAL)
def test_booked_room_is_excluded_from_matching_availability_search(
    room_client: RoomClient,
    api_assertions: ApiAssertions,
    room_assertions: RoomAssertions,
    created_booking: CreatedBooking,
) -> None:
    response = room_client.get_rooms(
        check_in=created_booking.request.dates.check_in,
        check_out=created_booking.request.dates.check_out,
    )

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="Room discovery should support filtering by an occupied stay period",
    )
    api_assertions.matches_schema(response, "rooms")
    room_assertions.room_is_not_listed(
        RoomCollection.from_payload(response_json(response)),
        room_id=created_booking.booking.room_id,
    )


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known RBP defect: an unknown room returns 500 instead of 404",
    strict=True,
)
@allure.story("Room discovery")
@allure.title("Unknown room identifier returns not found")
@allure.severity(allure.severity_level.NORMAL)
def test_unknown_room_identifier_returns_not_found(
    room_client: RoomClient,
    api_assertions: ApiAssertions,
    missing_resource_id: int,
) -> None:
    response = room_client.get_room(missing_resource_id)

    api_assertions.has_status(
        response,
        HTTPStatus.NOT_FOUND,
        because="An unknown room identifier should not be reported as a server failure",
    )
