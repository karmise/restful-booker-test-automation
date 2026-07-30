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

_SETTING_NAMES = (
    "RBP_BASE_URL",
    "RBP_ADMIN_USERNAME",
    "RBP_ADMIN_PASSWORD",
    "RBP_ACTION_TIMEOUT_MS",
    "RBP_NAVIGATION_TIMEOUT_MS",
    "RBP_API_TIMEOUT_S",
)


def test_settings_use_safe_sandbox_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _SETTING_NAMES:
        monkeypatch.delenv(name, raising=False)

    settings = Settings.from_env()

    assert settings.base_url == "https://automationintesting.online"
    assert settings.admin_username == "admin"
    assert settings.admin_password == "password"
    assert settings.action_timeout_ms == 10_000
    assert settings.navigation_timeout_ms == 30_000
    assert settings.api_timeout_s == 15


def test_settings_apply_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RBP_BASE_URL", "https://example.test/")
    monkeypatch.setenv("RBP_ADMIN_USERNAME", "operator")
    monkeypatch.setenv("RBP_ADMIN_PASSWORD", "not-a-real-secret")
    monkeypatch.setenv("RBP_ACTION_TIMEOUT_MS", "2500")
    monkeypatch.setenv("RBP_NAVIGATION_TIMEOUT_MS", "9000")
    monkeypatch.setenv("RBP_API_TIMEOUT_S", "3")

    settings = Settings.from_env()

    assert settings.base_url == "https://example.test"
    assert settings.admin_username == "operator"
    assert settings.admin_password == "not-a-real-secret"
    assert settings.action_timeout_ms == 2500
    assert settings.navigation_timeout_ms == 9000
    assert settings.api_timeout_s == 3


def test_settings_reject_non_positive_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RBP_API_TIMEOUT_S", "0")

    with pytest.raises(ValueError, match="RBP_API_TIMEOUT_S must be greater than zero"):
        Settings.from_env()
