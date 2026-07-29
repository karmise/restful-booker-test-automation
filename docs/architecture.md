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

### Fixtures

Compose settings, models, pages, and Playwright lifecycle objects. Fixture
modules are split by responsibility under `tests/ui/fixtures`. They are
registered by `tests/ui/conftest.py`, which prevents future API tests from
loading Playwright-specific fixtures.

### Tests

Describe scenarios through actions and domain assertions. Tests do not import
Playwright `expect`, contain raw CSS or XPath selectors, or instantiate page
objects and assertion objects directly.

## Deferred layers

API clients, API DTOs, and API fixtures are deliberately absent. They will be
introduced as a separate milestone so the UI framework does not pretend to have
an API architecture before API testing requirements are defined. A future API
suite can use `tests/api/fixtures` and `tests/api/conftest.py` without changing
the current UI imports.
