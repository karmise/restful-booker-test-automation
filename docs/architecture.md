# Architecture

## Design goals

The framework is optimized for readability, isolation, debuggability, and
controlled growth. Each layer has one direction of dependency.

```text
tests/ui
  |
  +-- tests/ui/fixtures
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
  +-- tests/api/fixtures
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
modules are split by responsibility under `tests/ui/fixtures` and
`tests/api/fixtures`. Their separate `conftest.py` files prevent API tests from
loading Playwright-specific fixtures.

API resource fixtures own mutation prerequisites and cleanup. A booking fixture
depends on a created room fixture, so pytest automatically deletes the booking
before deleting its room. Cleanup status is validated and failures are reported
as teardown errors instead of silently leaking test data.

### Reporting

Allure is integrated at the test orchestration boundary instead of inside page
objects, components, DTOs, or HTTP transport. Tests own business-level steps and
behavior metadata; resource fixtures own preparation and cleanup steps. This
keeps reporting concerns out of lower layers and prevents decorated function
arguments from exposing passwords, tokens, or complete DTO values as Allure
parameters.

Every pytest run writes fresh structured results to `allure-results`. API logs
are captured as attachments, failed UI scenarios attach the final full-page
screenshot, and a session hook records stable execution environment properties.
The Allure CLI converts these result files into the ignored `allure-report`
HTML artifact.

### Tests

Describe scenarios through actions and domain assertions. Tests do not import
Playwright `expect`, contain raw CSS or XPath selectors, or instantiate page
objects and assertion objects directly.

API tests also avoid raw URL construction, untyped dictionaries, direct
`jsonschema` calls, and assertions embedded in service clients.
