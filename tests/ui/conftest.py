"""Fixture plugin registration scoped to the UI test suite."""

pytest_plugins = (
    "tests.ui.fixtures.configuration",
    "tests.ui.fixtures.data",
    "tests.ui.fixtures.pages",
)
