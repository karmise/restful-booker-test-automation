"""Authentication API scenarios."""

from http import HTTPStatus

import allure
import pytest

from restful_booker.api.assertions import ApiAssertions, AuthAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import AuthClient
from restful_booker.api.dto import AuthRequest, TokenResponse

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("API tests"),
    allure.sub_suite("Authentication service"),
    allure.epic("REST API"),
    allure.feature("Authentication service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Token issuance")
@allure.title("Valid credentials return the token contract")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_credentials_return_token_contract(
    auth_client: AuthClient,
    api_assertions: ApiAssertions,
    auth_assertions: AuthAssertions,
    valid_api_credentials: AuthRequest,
) -> None:
    response = auth_client.login(valid_api_credentials)

    api_assertions.has_status(
        response,
        HTTPStatus.OK,
        because="Valid administrator credentials should be accepted",
    )
    api_assertions.matches_schema(response, "auth_login")
    auth_assertions.token_was_issued(TokenResponse.from_payload(response_json(response)))


@pytest.mark.api
@pytest.mark.regression
@allure.story("Credential validation")
@allure.title("Invalid credentials are rejected")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_credentials_are_rejected(
    auth_client: AuthClient,
    api_assertions: ApiAssertions,
    invalid_api_credentials: AuthRequest,
) -> None:
    response = auth_client.login(invalid_api_credentials)

    api_assertions.has_status(
        response,
        HTTPStatus.UNAUTHORIZED,
        because="Invalid administrator credentials must not create a token",
    )
    api_assertions.contains_error(response, "Invalid credentials")


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Token validation")
@allure.title("A newly issued token is accepted by validation")
@allure.severity(allure.severity_level.CRITICAL)
def test_issued_token_is_accepted_by_validation(
    auth_client: AuthClient,
    api_assertions: ApiAssertions,
    auth_assertions: AuthAssertions,
    valid_api_credentials: AuthRequest,
) -> None:
    login_response = auth_client.login(valid_api_credentials)
    api_assertions.has_status(
        login_response,
        HTTPStatus.OK,
        because="Token validation requires a successful login",
    )
    token = TokenResponse.from_payload(response_json(login_response))

    validation_response = auth_client.validate(token.token)

    api_assertions.has_status(
        validation_response,
        HTTPStatus.OK,
        because="A freshly issued authentication token should be valid",
    )
    auth_assertions.token_is_valid(response_json(validation_response))
