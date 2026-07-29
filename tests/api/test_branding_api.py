"""Branding API scenarios."""

from http import HTTPStatus

import pytest

from restful_booker.api.assertions import ApiAssertions, BrandingAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import BrandingClient


@pytest.mark.api
@pytest.mark.smoke
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
