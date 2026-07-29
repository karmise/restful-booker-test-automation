# Restful Booker UI Test Framework

A layered Python test automation framework for the
[Restful Booker Platform](https://automationintesting.online).

The UI milestone contains 15 tests: five scenarios for each of the home,
reservation, and administration areas. API automation is intentionally outside
the current milestone.

## Architecture

The framework separates test intent from browser mechanics:

```text
tests/ui
  -> UI fixtures
    -> assertion objects
      -> page objects
        -> reusable UI components
    -> test-data factories and UI models
      -> Playwright
```

- `core` owns environment configuration.
- `models` contains immutable data passed between test layers.
- `testdata` creates valid and unique test inputs.
- `ui/assertions` contains domain checks and readable failure messages.
- `ui/components` represents reusable or behavior-rich page elements.
- `ui/pages` exposes business-oriented page actions.
- `tests/ui/fixtures` composes UI objects and controls their lifecycle.
- `tests/ui` contains browser scenarios and assertions.

Fixture registration is scoped by test type. UI fixtures are registered in
`tests/ui/conftest.py`, so a future `tests/api` suite will not load Playwright
fixtures or depend on browser setup.

The project deliberately has no generic `helpers` module or inheritance-heavy
base page. Shared abstractions will be introduced only when real duplication
demonstrates a stable responsibility.

Tests do not import Playwright `expect`. Assertion objects retain Playwright's
native expected/actual values and call logs while adding business context.

See [Architecture](docs/architecture.md) and
[UI test plan](docs/ui-test-plan.md) for the current design. Locator decisions
are documented separately in the
[locator strategy](docs/locator-strategy.md).

## Prerequisites

- Python 3.12
- Poetry 2.x

## Local setup

```bash
poetry env use 3.12
poetry install
poetry run playwright install chromium
```

Copy `.env.example` to `.env` only when execution settings need to be
overridden. The public sandbox credentials are intentionally non-secret.

## Running checks

```bash
poetry run ruff format --check .
poetry run ruff check .
poetry run mypy src tests
poetry run pytest tests/ui
```

Run an individual area:

```bash
poetry run pytest tests/ui/test_home_page.py
```

The pytest configuration retains a Playwright trace and screenshot for failed
tests under `artifacts/`.

## Implemented UI coverage

| Area | Scenarios |
| --- | --- |
| Home | Open a room, Contact navigation, required and format validation, valid message |
| Reservation | Room details, pricing, required and format validation, cancel guest entry |
| Administration | Invalid and valid login, route protection, Report navigation, logout |

The GitHub Actions workflow runs formatting, linting, type checking, and all 15
tests in Chromium on Python 3.12. Failure artifacts are retained for seven days.

## Environment variables

| Variable | Default |
| --- | --- |
| `RBP_BASE_URL` | `https://automationintesting.online` |
| `RBP_ADMIN_USERNAME` | `admin` |
| `RBP_ADMIN_PASSWORD` | `password` |
| `RBP_ACTION_TIMEOUT_MS` | `10000` |
| `RBP_NAVIGATION_TIMEOUT_MS` | `30000` |

The public environment is shared and periodically reset. Tests therefore use
isolated browser contexts, unique generated form data, and avoid destructive
administration scenarios.
