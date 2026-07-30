"""Branding API scenarios."""

from http import HTTPStatus

import allure
import pytest

from restful_booker.api.assertions import ApiAssertions, BrandingAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import BrandingClient

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("API tests"),
    allure.sub_suite("Branding service"),
    allure.epic("REST API"),
    allure.feature("Branding service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Public branding")
@allure.title("Branding matches the public contract")
@allure.severity(allure.severity_level.NORMAL)
def test_branding_matches_public_contract(
    branding_client: BrandingClient,
    api_assertions: ApiAssertions,
    branding_assertions: BrandingAssertions,
) -> None:
    response = branding_client.get_branding()

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="Public pages require branding and contact information",
    )
    api_assertions.matches_schema(response, "branding")
    branding_assertions.identifies_property(response_json(response))
