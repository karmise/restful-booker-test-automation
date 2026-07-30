"""Contact-message API scenarios."""

from http import HTTPStatus

import allure
import pytest

from restful_booker.api.assertions import ApiAssertions, MessageAssertions
from restful_booker.api.clients import MessageClient
from restful_booker.api.dto import MessageRequest
from tests.api.fixtures.resources import CreatedMessage

pytestmark = [
    allure.epic("REST API"),
    allure.feature("Message service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Contact message creation")
@allure.title("Guest can create a contact message")
@allure.severity(allure.severity_level.CRITICAL)
def test_guest_can_create_contact_message(
    created_message: CreatedMessage,
    api_assertions: ApiAssertions,
    message_assertions: MessageAssertions,
) -> None:
    with allure.step("Verify that the contact message was accepted and is discoverable"):
        api_assertions.has_status(
            created_message.create_response,
            HTTPStatus.OK,
            because="A valid public contact message should be accepted",
        )
        api_assertions.success_flag_is_true(created_message.create_response)
        api_assertions.matches_schema(created_message.collection_response, "messages")
        message_assertions.created_message_matches(
            created_message.message,
            created_message.request,
        )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Contact message validation")
@allure.title("Contact message rejects an invalid email")
@allure.severity(allure.severity_level.NORMAL)
def test_message_rejects_invalid_email(
    message_client: MessageClient,
    api_assertions: ApiAssertions,
    invalid_message_request: MessageRequest,
) -> None:
    with allure.step("Submit a contact message with an invalid email"):
        response = message_client.create_message(invalid_message_request)

    with allure.step("Verify the email validation error"):
        api_assertions.has_status(
            response,
            HTTPStatus.BAD_REQUEST,
            because="A malformed contact email must not be persisted",
        )
        api_assertions.contains_error(response, "well-formed email")


@pytest.mark.api
@pytest.mark.regression
@allure.story("Message authorization")
@allure.title("Anonymous user cannot delete a message")
@allure.severity(allure.severity_level.CRITICAL)
def test_anonymous_user_cannot_delete_message(
    message_client: MessageClient,
    api_assertions: ApiAssertions,
    created_message: CreatedMessage,
) -> None:
    with allure.step("Attempt to delete a message without authentication"):
        response = message_client.delete_message(created_message.message.message_id)

    with allure.step("Verify that anonymous deletion is forbidden"):
        api_assertions.has_status(
            response,
            HTTPStatus.FORBIDDEN,
            because="Only an authenticated administrator may delete contact messages",
        )
