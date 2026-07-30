"""Cross-suite reporting hooks."""

import platform
from pathlib import Path

import pytest

from restful_booker.core import Settings


def pytest_sessionfinish(session: pytest.Session) -> None:
    """Add stable execution context to the generated Allure results."""

    results_directory = session.config.getoption("--alluredir")
    if not results_directory:
        return

    settings = Settings.from_env()
    environment = {
        "Base URL": settings.base_url,
        "Operating system": platform.platform(),
        "Python": platform.python_version(),
    }
    rendered = "\n".join(f"{key}={value}" for key, value in environment.items())
    results_path = Path(results_directory)
    results_path.mkdir(parents=True, exist_ok=True)
    (results_path / "environment.properties").write_text(
        f"{rendered}\n",
        encoding="utf-8",
    )
