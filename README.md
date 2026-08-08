# Restful Booker Test Automation Framework

[![Test automation](https://github.com/karmise/restful-booker-test-automation/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/karmise/restful-booker-test-automation/actions/workflows/tests.yml)
[![Allure report](https://img.shields.io/badge/Allure_report-live-ff4088?logo=qameta)](https://karmise.github.io/restful-booker-test-automation/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776ab?logo=python&logoColor=white)](https://www.python.org/)

A layered Python test automation framework for the
[Restful Booker Platform](https://automationintesting.online).

The project contains 60 automated tests: 15 browser scenarios, 26 API
scenarios covering six external service contracts, and 19 fast unit tests for
the framework itself.

**[Open the latest interactive Allure report](https://karmise.github.io/restful-booker-test-automation/)**

## Architecture

The framework separates test intent from transport mechanics:

```text
tests/ui
  -> fixtures/ui
    -> assertion objects
      -> page objects
        -> reusable UI components
    -> test-data factories and UI models
      -> Playwright

tests/api
  -> fixtures/api
    -> assertion objects and JSON Schemas
      -> service clients
        -> request and response DTOs
          -> requests.Session

tests/unit
  -> isolated checks for framework contracts
    -> DTOs, configuration, schema validation, logging, and reporting
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
- `api/resource_lifecycle` guarantees reverse-order cleanup after partial failures.
- `fixtures/ui` composes UI objects and API-backed test-data preconditions.
- `fixtures/api` authenticates and registers test-owned resource cleanup.
- `tests/unit` verifies framework behavior without a browser or network.

Fixture registration is scoped by test type. API tests never load Playwright
fixtures. UI test bodies remain browser-only; API clients are used only by
fixtures to create and remove isolated preconditions.

The project deliberately has no generic `helpers` module or inheritance-heavy
base page. Shared abstractions will be introduced only when real duplication
demonstrates a stable responsibility.

Tests do not import Playwright `expect`. Assertion objects retain Playwright's
native expected/actual values and call logs while adding business context.

See [Architecture](docs/architecture.md),
[testing conventions](docs/testing-conventions.md),
[UI test plan](docs/ui-test-plan.md), and
[API test plan](docs/api-test-plan.md). Locator decisions are documented in the
[locator strategy](docs/locator-strategy.md).

## Prerequisites

- Python 3.12
- Poetry 2.x
- Allure Report CLI and Java 8+ to render or open HTML reports

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
poetry run mypy src fixtures tests
poetry run pytest tests/unit
poetry run pytest tests/api
poetry run pytest tests/ui
```

Run an individual area:

```bash
poetry run pytest tests/ui/test_home_page.py
poetry run pytest tests/api/test_booking_api.py
```

Every pytest run replaces `allure-results/` with fresh Allure result files.

## Allure reports

Tests are organized in two parallel Allure hierarchies:
`parent suite → suite → sub-suite` for UI/API module navigation and
`epic → feature → story` for behavior navigation. Test modules own only
metadata. Reusable page actions, API clients, and assertion objects emit the
high-level steps, keeping reporting statements out of test bodies. API
lifecycle operations appear as setup and cleanup steps, Python logs are
attached automatically, and failed UI tests include a full-page
screenshot. The report also records the base URL, operating system, and Python
version.

Install the Allure command-line tool on macOS:

```bash
brew install allure
allure --version
```

Run any test scope and open a temporary report:

```bash
poetry run pytest tests/api
allure serve allure-results
```

Generate a persistent HTML report:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

`allure-pytest` is managed by Poetry and writes structured results.
The separately installed Allure CLI converts those results into HTML.
Both `allure-results/` and `allure-report/` are local generated artifacts and
are excluded from Git.

## API request logging

The shared API transport logs the request method, URL, query parameters,
headers, cookie names, request body, response status, elapsed time, response
headers, and response body. Passwords, tokens, authorization headers, and cookie
values are replaced with `<redacted>`. Bodies longer than 4,000 characters are
truncated.

By default, pytest captures `INFO` logs and prints them when a test fails. To
stream every request and response during a local run:

```bash
poetry run pytest tests/api --log-cli-level=INFO
```

To keep live logging enabled for every run, change this option in
`pyproject.toml`:

```toml
[tool.pytest.ini_options]
log_cli = true
```

Set it back to `false` to return to failure-only output. The same options could
live in `pytest.ini`; this project keeps all Python tool configuration in one
`pyproject.toml`.

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
| Auth | Token contract, credential validation, valid and unknown tokens |
| Room | Collection and item discovery, creation, authorization, date availability |
| Booking | Creation and item discovery, validation, authorization, overlap conflict |
| Message | Creation and item discovery, validation, authorization, read-state transition |
| Branding | Public branding contract and business identity |
| Report | Empty room availability and a booked unavailable period |

Six Draft 2020-12 schemas validate the external contracts consumed by the UI.
Lifecycle fixtures register unique rooms, bookings, and messages before the
mutation request, then remove them in reverse dependency order even if later
discovery, contract validation, or the test itself fails. UI data preconditions
use the same lifecycle without exposing API clients in browser-test bodies.
Two strict expected-failure scenarios document known sandbox defects where
unknown room and message identifiers return `500` instead of `404`.

## Continuous integration

GitHub Actions uses one event-aware workflow instead of treating every change
as a full regression run:

| Trigger | Test selection | Browsers | Published report |
| --- | --- | --- | --- |
| Pull request | Quality, unit, API smoke, UI smoke | Chromium | Raw Allure artifacts |
| Push to `main` | Quality, unit, full API, full UI | Chromium | Pages + Allure history |
| Daily schedule | Quality, unit, full API, full UI | Chromium, Firefox, WebKit | Pages + Allure history |
| Manual dispatch | Selected layer and marker | Selected browser or all | Raw Allure artifacts |

The scheduled workflow starts at `02:00 UTC` (`08:00` in Bishkek). A manual
run can select `api`, `ui`, or both; `smoke`, `regression`, or all scenarios;
one browser or the complete browser matrix; a target base URL; and optional
console HTTP logging. Quality and framework unit checks run in every mode. A
separate health gate verifies the target environment before API and UI jobs,
so an unavailable public sandbox is distinguishable from a product-test
failure. Pull requests stay fast while `main` and nightly runs retain complete
regression coverage.

Every test job uploads independent Allure results. Browser traces, screenshots,
and other Playwright diagnostics are retained on failure. Raw artifacts are
kept for 30 days. Trusted automatic runs restore Allure history, merge their
results into the live report, and retain the latest 20 complete reports.
Previous launches open from the report's `Trends` widgets. The automatically
managed `allure-history` branch stores the generated reports; GitHub Pages
remains configured to deploy with GitHub Actions.

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
isolated browser contexts and unique generated data. API-backed cleanup deletes
only resources registered by the current API or UI test.
