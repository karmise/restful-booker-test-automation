"""Contact-message API scenarios."""

from http import HTTPStatus

import allure
import pytest

from fixtures.api.resources import CreatedMessage, wait_for_message
from restful_booker.api.assertions import ApiAssertions, MessageAssertions
from restful_booker.api.assertions.api_assertions import response_json
from restful_booker.api.clients import MessageClient
from restful_booker.api.dto import MessageCollection, MessageRequest
from restful_booker.api.resource_lifecycle import ApiResourceLifecycle
from restful_booker.api.testdata import ApiTestDataFactory

pytestmark = [
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("API tests"),
    allure.sub_suite("Message service"),
    allure.epic("REST API"),
    allure.feature("Message service"),
]


@pytest.mark.api
@pytest.mark.smoke
@allure.story("Contact message creation")
@allure.title("Guest can create a contact message")
@allure.severity(allure.severity_level.CRITICAL)
def test_guest_can_create_contact_message(
    message_client: MessageClient,
    admin_message_client: MessageClient,
    api_test_data_factory: ApiTestDataFactory,
    api_resource_lifecycle: ApiResourceLifecycle,
    api_assertions: ApiAssertions,
    message_assertions: MessageAssertions,
) -> None:
    request = api_test_data_factory.message_request()

    api_resource_lifecycle.track_message(subject=request.subject)
    create_response = message_client.create_message(request)

    api_assertions.has_status(
        create_response,
        HTTPStatus.OK,
        because="A valid public contact message should be accepted",
    )
    api_assertions.success_flag_is_true(create_response)

    discovered = wait_for_message(admin_message_client, subject=request.subject)
    collection_response = discovered.response
    api_assertions.has_status(
        collection_response,
        HTTPStatus.OK,
        because="The created message should be discoverable by the administrator",
    )
    api_assertions.matches_schema(collection_response, "messages")
    message = discovered.message
    api_resource_lifecycle.track_message(
        subject=request.subject,
        message_id=message.message_id,
    )
    message_assertions.created_message_matches(message, request)


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
    response = message_client.create_message(invalid_message_request)

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
    response = message_client.delete_message(created_message.message.message_id)

    api_assertions.has_status(
        response,
        HTTPStatus.FORBIDDEN,
        because="Only an authenticated administrator may delete contact messages",
    )


@pytest.mark.api
@pytest.mark.regression
@allure.story("Message administration")
@allure.title("Administrator can mark a contact message as read")
@allure.severity(allure.severity_level.NORMAL)
def test_administrator_can_mark_contact_message_as_read(
    admin_message_client: MessageClient,
    message_client: MessageClient,
    api_assertions: ApiAssertions,
    message_assertions: MessageAssertions,
    created_message: CreatedMessage,
) -> None:
    update_response = admin_message_client.mark_as_read(
        created_message.message.message_id,
    )
    collection_response = message_client.get_messages()

    api_assertions.has_status(
        update_response,
        HTTPStatus.ACCEPTED,
        because="An administrator should be able to acknowledge a contact message",
    )
    api_assertions.has_status(
        collection_response,
        HTTPStatus.OK,
        because="The updated contact message should remain discoverable",
    )
    message_assertions.message_is_read(
        MessageCollection.from_payload(response_json(collection_response)).find_by_subject(
            created_message.request.subject
        )
    )


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known RBP defect: an unknown message returns 500 instead of 404",
    strict=True,
)
@allure.story("Message discovery")
@allure.title("Unknown message identifier returns not found")
@allure.severity(allure.severity_level.NORMAL)
def test_unknown_message_identifier_returns_not_found(
    admin_message_client: MessageClient,
    api_assertions: ApiAssertions,
    missing_resource_id: int,
) -> None:
    response = admin_message_client.get_message(missing_resource_id)

    api_assertions.has_status(
        response,
        HTTPStatus.NOT_FOUND,
        because="An unknown message identifier should not be reported as a server failure",
    )
