"""Room report API scenarios."""

from http import HTTPStatus

import allure
import pytest

from fixtures.api.resources import CreatedBooking, CreatedRoom
from restful_booker.api.assertions import ApiAssertions, ReportAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import ReportClient

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("API tests"),
    allure.sub_suite("Report service"),
    allure.epic("REST API"),
    allure.feature("Report service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Room availability")
@allure.title("New room report matches the public contract")
@allure.severity(allure.severity_level.NORMAL)
def test_new_room_report_matches_contract(
    report_client: ReportClient,
    api_assertions: ApiAssertions,
    report_assertions: ReportAssertions,
    created_room: CreatedRoom,
) -> None:
    response = report_client.get_room_report(created_room.room.room_id)

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="The reservation calendar requires a room availability report",
    )
    api_assertions.matches_schema(response, "report")
    report_assertions.has_no_entries_for_new_room(response_json(response))


@pytest.mark.api
@pytest.mark.regression
@allure.story("Room availability")
@allure.title("Created booking appears as an unavailable room period")
@allure.severity(allure.severity_level.CRITICAL)
def test_created_booking_appears_as_unavailable_room_period(
    report_client: ReportClient,
    api_assertions: ApiAssertions,
    report_assertions: ReportAssertions,
    created_booking: CreatedBooking,
) -> None:
    response = report_client.get_room_report(created_booking.booking.room_id)

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="A confirmed booking should block the same dates in the reservation calendar",
    )
    api_assertions.matches_schema(response, "report")
    report_assertions.contains_unavailable_period(
        response_json(response),
        created_booking.request.dates,
    )
