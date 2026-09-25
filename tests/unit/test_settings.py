"""Unit tests for environment-backed framework settings."""

import allure
import pytest

from restful_booker.core import Settings

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Configuration"),
    allure.epic("Test framework"),
    allure.feature("Configuration"),
]


def test_settings_use_safe_sandbox_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "RBP_BASE_URL",
        "RBP_ADMIN_USERNAME",
        "RBP_ADMIN_PASSWORD",
        "RBP_ACTION_TIMEOUT_MS",
        "RBP_NAVIGATION_TIMEOUT_MS",
        "RBP_API_TIMEOUT_S",
        "RBP_API_CONNECT_TIMEOUT_S",
    ):
        monkeypatch.delenv(name, raising=False)

    settings = Settings.from_env()

    assert settings.base_url == "https://automationintesting.online"
    assert settings.admin_username == "admin"
    assert settings.admin_password == "password"
    assert settings.action_timeout_ms == 10_000
    assert settings.navigation_timeout_ms == 30_000
    assert settings.api_timeout_s == 15
    assert settings.api_timeout == (5, 15)


def test_settings_apply_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RBP_BASE_URL", "https://example.test/")
    monkeypatch.setenv("RBP_ADMIN_USERNAME", "operator")
    monkeypatch.setenv("RBP_ADMIN_PASSWORD", "not-a-real-secret")
    monkeypatch.setenv("RBP_ACTION_TIMEOUT_MS", "2500")
    monkeypatch.setenv("RBP_NAVIGATION_TIMEOUT_MS", "9000")
    monkeypatch.setenv("RBP_API_TIMEOUT_S", "3")
    monkeypatch.setenv("RBP_API_CONNECT_TIMEOUT_S", "2")

    settings = Settings.from_env()

    assert settings.base_url == "https://example.test"
    assert settings.admin_username == "operator"
    assert settings.admin_password == "not-a-real-secret"
    assert settings.action_timeout_ms == 2500
    assert settings.navigation_timeout_ms == 9000
    assert settings.api_timeout_s == 3
    assert settings.api_timeout == (2, 3)


@pytest.mark.parametrize("value", ["0", "-1", "invalid", "1.5", ""])
def test_settings_reject_invalid_connect_timeout(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    monkeypatch.setenv("RBP_API_CONNECT_TIMEOUT_S", value)
    with pytest.raises(ValueError, match="RBP_API_CONNECT_TIMEOUT_S"):
        Settings.from_env()


@pytest.mark.parametrize(
    "value",
    [
        "",
        "example.test",
        "ftp://example.test",
        "https://user:secret@example.test",
        "https://example.test?token=secret",
        "https://example.test/#section",
        "https://example.test:invalid",
        "https://bad host.test",
    ],
)
def test_settings_reject_invalid_base_url(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("RBP_BASE_URL", value)
    with pytest.raises(ValueError, match="RBP_BASE_URL") as caught:
        Settings.from_env()
    assert "secret" not in str(caught.value)


def test_settings_hide_password_in_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RBP_ADMIN_PASSWORD", "private-credential")
    settings = Settings.from_env()
    assert "private-credential" not in repr(settings)
    assert settings.admin_password == "private-credential"


def test_settings_reject_non_positive_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RBP_API_TIMEOUT_S", "0")

    with pytest.raises(ValueError, match="RBP_API_TIMEOUT_S must be greater than zero"):
        Settings.from_env()
