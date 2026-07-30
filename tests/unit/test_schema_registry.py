"""Unit tests for readable JSON Schema diagnostics."""

import allure
import pytest

from restful_booker.api.schema_registry import SchemaRegistry

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Schema validation"),
    allure.epic("Test framework"),
    allure.feature("JSON Schema validation"),
]

_AUTH_SCHEMA = "auth_login"


def test_schema_registry_accepts_valid_contract() -> None:
    SchemaRegistry().validate({"token": "a-secure-token-value"}, _AUTH_SCHEMA)


def test_schema_registry_reports_every_violation_with_json_path() -> None:
    with pytest.raises(AssertionError) as error:
        SchemaRegistry().validate(
            {"token": 123, "unexpected": True},
            _AUTH_SCHEMA,
        )

    message = str(error.value)
    assert f"Response does not match JSON Schema '{_AUTH_SCHEMA}'" in message
    assert "$: Additional properties are not allowed ('unexpected' was unexpected)" in message
    assert "$.token: 123 is not of type 'string'" in message
