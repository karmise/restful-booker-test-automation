# Restful Booker Test Automation Framework

A layered Python test automation framework for the
[Restful Booker Platform](https://automationintesting.online).

The project contains 30 automated tests: 15 browser scenarios and 15 API
scenarios covering six external service contracts.

## Architecture

The framework separates test intent from transport mechanics:

```text
tests/ui
  -> UI fixtures
    -> assertion objects
      -> page objects
        -> reusable UI components
    -> test-data factories and UI models
      -> Playwright

tests/api
  -> API fixtures and resource lifecycles
    -> assertion objects and JSON Schemas
      -> service clients
        -> request and response DTOs
          -> requests.Session
```

- `core` owns environment configuration.
- `models` and `testdata` contain typed UI data.
- `ui/assertions` contains domain checks and readable failure messages.
- `ui/components` represents reusable or behavior-rich page elements.
- `ui/pages` exposes business-oriented page actions.
- `api/dto` contains immutable external API contracts.
- `api/clients` contains one HTTP client per service.
- `api/schemas` contains Draft 2020-12 JSON Schemas.
- `api/assertions` separates protocol, contract, and business checks.
- `api/testdata` creates unique API-owned resources.
- `tests/ui/fixtures` composes UI objects and controls their lifecycle.
- `tests/api/fixtures` authenticates and guarantees reverse-order cleanup.

Fixture registration is scoped by test type. API tests never load Playwright
fixtures, and UI tests do not create HTTP clients.

The project deliberately has no generic `helpers` module or inheritance-heavy
base page. Shared abstractions will be introduced only when real duplication
demonstrates a stable responsibility.

Tests do not import Playwright `expect`. Assertion objects retain Playwright's
native expected/actual values and call logs while adding business context.

See [Architecture](docs/architecture.md), [UI test plan](docs/ui-test-plan.md),
and [API test plan](docs/api-test-plan.md). Locator decisions are documented in
the [locator strategy](docs/locator-strategy.md).

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
poetry run pytest tests/api
poetry run pytest tests/ui
```

Run an individual area:

```bash
poetry run pytest tests/ui/test_home_page.py
poetry run pytest tests/api/test_booking_api.py
```

The pytest configuration retains a Playwright trace and screenshot for failed
tests under `artifacts/`.

## Implemented UI coverage

| Area | Scenarios |
| --- | --- |
| Home | Open a room, Contact navigation, required and format validation, valid message |
| Reservation | Room details, pricing, required and format validation, cancel guest entry |
| Administration | Invalid and valid login, route protection, Report navigation, logout |

## Implemented API coverage

| Service | Scenarios |
| --- | --- |
| Auth | Token contract, invalid credentials, token validation |
| Room | Collection contract, isolated creation, authorization |
| Booking | Isolated creation, field and date validation, authorization |
| Message | Isolated creation, email validation, authorization |
| Branding | Public branding contract and business identity |
| Report | Empty availability report for a newly created room |

Six Draft 2020-12 schemas validate the external contracts consumed by the UI.
Lifecycle fixtures create unique rooms, bookings, and messages, then remove
them in reverse dependency order even after a failed assertion.

GitHub Actions runs quality checks, the API suite, and the Chromium UI suite as
separate jobs on Python 3.12. Browser failure artifacts are retained for seven
days.

## Environment variables

| Variable | Default |
| --- | --- |
| `RBP_BASE_URL` | `https://automationintesting.online` |
| `RBP_ADMIN_USERNAME` | `admin` |
| `RBP_ADMIN_PASSWORD` | `password` |
| `RBP_ACTION_TIMEOUT_MS` | `10000` |
| `RBP_NAVIGATION_TIMEOUT_MS` | `30000` |
| `RBP_API_TIMEOUT_S` | `15` |

The public environment is shared and periodically reset. Tests therefore use
isolated browser contexts and unique generated data. API cleanup deletes only
resources created by the current test.
