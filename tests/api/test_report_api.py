"""Room report API scenarios."""

from http import HTTPStatus

import pytest

from restful_booker.api.assertions import ApiAssertions, ReportAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import ReportClient
from tests.api.fixtures.resources import CreatedRoom


@pytest.mark.api
@pytest.mark.smoke
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
