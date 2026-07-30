"""Unit tests for the secret-safe Allure step adapter."""

from contextlib import nullcontext

import allure
import pytest

from restful_booker.reporting import steps

pytestmark = [
    pytest.mark.unit,
    allure.parent_suite("Restful Booker Platform"),
    allure.suite("Framework unit tests"),
    allure.sub_suite("Reporting"),
    allure.epic("Test framework"),
    allure.feature("Allure step adapter"),
]


def test_report_step_uses_fixed_title_and_preserves_function_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded_titles: list[str] = []

    def fake_step(title: str) -> nullcontext[None]:
        recorded_titles.append(title)
        return nullcontext()

    monkeypatch.setattr(steps.allure, "step", fake_step)

    @steps.report_step("Authenticate administrator")
    def authenticate(username: str, password: str) -> str:
        """Return a synthetic token."""
        return f"{username}:{password}"

    assert authenticate("admin", "secret") == "admin:secret"
    assert recorded_titles == ["Authenticate administrator"]
    assert authenticate.__name__ == "authenticate"
    assert authenticate.__doc__ == "Return a synthetic token."


def test_report_step_propagates_wrapped_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(steps.allure, "step", lambda title: nullcontext())

    @steps.report_step("Failing operation")
    def failing_operation() -> None:
        raise RuntimeError("original failure")

    with pytest.raises(RuntimeError, match="original failure"):
        failing_operation()
