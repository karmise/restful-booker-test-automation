# Architecture

## Design goals

The framework is optimized for readability, isolation, debuggability, and
controlled growth. Each layer has one direction of dependency.

```text
tests/ui
  |
  +-- tests/ui/conftest.py
        |
        +-- fixtures/ui
              |
              +-- restful_booker.testdata
              +-- restful_booker.models
              +-- restful_booker.ui.assertions
                    |
                    +-- restful_booker.ui.pages
                          |
                          +-- restful_booker.ui.components
                                |
                                +-- Playwright

tests/api
  |
  +-- tests/api/conftest.py
        |
        +-- fixtures/api
              |
              +-- restful_booker.api.testdata
              +-- restful_booker.api.assertions
                    |
                    +-- restful_booker.api.schema_registry
                    +-- restful_booker.api.clients
                          |
                          +-- restful_booker.api.dto
                                |
                                +-- requests.Session

tests/unit
  |
  +-- isolated framework contracts
        |
        +-- DTO parsing and serialization
        +-- settings validation
        +-- JSON Schema diagnostics
        +-- safe HTTP logging
        +-- reporting adapter
```

Lower layers never import tests or fixtures.

## Layer responsibilities

### Core

Loads and validates execution settings. Environment access is isolated here so
that page objects and tests do not read environment variables directly.

### Models

Immutable UI input objects such as credentials, contact messages, stay periods,
and guest details. These are not API DTOs. Their purpose is to give fixtures and
page objects typed contracts instead of passing loosely related dictionaries.

### API DTOs

Immutable request and response contracts use Python field names internally and
serialize explicitly to the external JSON field names. Response DTOs parse
schema-validated payloads used for resource discovery and business assertions.

### Test data

Creates valid, unique model instances. Generation rules remain outside tests,
which keeps scenarios focused on behavior.

### UI components

Represents reusable or behavior-rich parts of a screen, such as navigation,
contact forms, and booking calendars. Components own their locators and browser
interactions.

### Page objects

Represents complete application pages and coordinates components. Page objects
expose user-oriented actions and observable elements. They do not contain test
cases or assertions.

### Assertion objects

Group observable outcomes by business area. They are the only UI framework
modules that import Playwright `expect`. Each expectation keeps Playwright's
native diagnostics and adds a user-facing message describing the failed
business condition. Generic wrappers such as `assert_visible(locator)` are
deliberately avoided.

API assertions are split into protocol checks, JSON Schema validation, and
service-specific business comparisons. HTTP clients never assert status codes
or hide raw responses.

### API clients

Each external service has a focused client built on a shared
`requests.Session` transport. The transport owns URL construction, connection
reuse, and request timeouts. Authentication is represented by a session cookie,
matching the contract used by the UI.

The same transport emits structured request and response diagnostics through
Python logging. Pytest controls whether logs are shown live or only attached to
failures. Sensitive headers, passwords, tokens, and cookie values are redacted
before formatting, so debug output can be retained in CI artifacts safely.

### JSON Schemas

Draft 2020-12 schemas describe the six external service responses. Schemas
reject missing, incorrectly typed, incorrectly formatted, and unexpected
properties. A cached registry reports every violation with its JSON path.

### Fixtures

Compose settings, models, pages, and Playwright lifecycle objects. Fixture
modules form a separate root layer split by responsibility under `fixtures/ui`
and `fixtures/api`. The suite-local `conftest.py` files only register the
appropriate branch, preventing API tests from loading Playwright-specific
fixtures.

API resource fixtures own mutation prerequisites and cleanup. A booking fixture
depends on a created room fixture, so pytest automatically deletes the booking
before deleting its room. Cleanup status is validated and failures are reported
as teardown errors instead of silently leaking test data.

### Reporting

Allure metadata stays at the test-module boundary, where tests declare both the
suite hierarchy (`parent suite → suite → sub-suite`) and behavior hierarchy
(`epic → feature → story`). Business steps are emitted by reusable page
actions, API client operations, and assertion objects, so test bodies remain
free of reporting contexts.

A small reporting adapter wraps those operations with fixed-title context
steps. Unlike the standard decorated-step API, it does not serialize wrapped
function arguments. Credentials, tokens, and complete DTO values therefore do
not become Allure step parameters. DTOs and raw HTTP transport remain unaware
of reporting.

Every pytest run writes fresh structured results to `allure-results`. API logs
are captured as attachments, failed UI scenarios attach the final full-page
screenshot, and a session hook records stable execution environment properties.
The Allure CLI converts these result files into the ignored `allure-report`
HTML artifact. CI merges the unit, API, and UI result artifacts into one report
and publishes it through GitHub Pages after runs on the default branch.

### Tests

Describe scenarios through actions and domain assertions. Tests do not import
Playwright `expect`, contain raw CSS or XPath selectors, or instantiate page
objects and assertion objects directly.

API tests also avoid raw URL construction, untyped dictionaries, direct
`jsonschema` calls, and assertions embedded in service clients.

Framework unit tests verify deterministic infrastructure behavior without
opening a browser or calling the public sandbox. This provides fast feedback
for contract parsing, configuration, schema diagnostics, secret redaction, and
reporting integration before the slower end-to-end suites run.
