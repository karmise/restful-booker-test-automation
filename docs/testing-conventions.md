# Testing conventions

## Assertion boundaries

Assertions are organized according to the scope of a test rather than forced
through one universal API.

UI and API scenarios use domain-oriented assertion objects. These objects add
business context, reusable Allure steps, and transport-specific diagnostics
while keeping scenario bodies focused on behavior. Generic wrappers such as
`assert_equal(actual, expected)` are avoided because they hide intent without
adding domain knowledge.

Framework unit tests use pytest's native `assert` and `pytest.raises` directly.
The expected value remains next to the operation under test, and pytest retains
its assertion introspection and structural diff. Moving those checks into a
shared assertion class would introduce another abstraction whose correctness
would itself need unit coverage.

## Expected application contracts

Expected API error messages, fixed response content, UI confirmation templates,
validation messages, and visible labels live in `src/restful_booker/contracts/`,
even when used by one scenario. Modules are grouped by transport and domain:

```text
contracts/
  api/
    auth.py          # authentication errors and valid-token response
    booking.py       # booking validation and conflict errors
    message.py       # contact validation and read-state expectations
    branding.py      # public property identity
    report.py        # availability report content
    mutation.py      # success envelope fields
  ui/
    authentication.py
    contact.py
    reservation.py
    home.py
    navigation.py
    calendar.py
```

Import the domain module with a descriptive name, for example:

```python
from restful_booker.contracts.api import auth as auth_contract

api_assertions.contains_error(response, auth_contract.INVALID_CREDENTIALS)
```

- Keep API and UI contracts separate even when text currently matches.
- Preserve exact versus substring matching at the assertion call site. API error
  fragments are explicitly documented as fragments, not complete error bodies.
- Use named placeholders for dynamic UI text, such as the contact sender's name.
- Define constants with `Final`; use immutable tuples and read-only mappings for
  shared collections. Return fresh expected payloads when nested lists are needed.
- Keep HTTP statuses as standard-library `HTTPStatus` members.
- Keep input data in factories/fixtures, separate from expected responses.
- Keep assertion explanations, Allure step titles, and locator descriptions at
  their call sites; these describe the test, not the application contract.
- Keep structural JSON field names, routes, selectors and test IDs in their
  owning transport/page/component/schema layers.
- Framework unit examples and expected framework diagnostics stay local to the
  unit tests. Never import the implementation's own constants as their oracle.

Contracts are test-owned expectations: they are not populated from actual
responses or imported from application implementation code. Update them only
when an intentional application contract change has been established, not to
make a failing test pass. There is no catch-all `constants.py` or container class.

## Scenario structure

Each test follows one path with one expected outcome. Split successful and
failing outcomes into separate tests instead of selecting assertions with
`if/elif/else`. Use parametrization for different inputs that share the same
assertion shape. Reusable assertion logic belongs in the assertion layer;
fixture and transport lifecycle decisions belong in their respective layers.

Known sandbox behavior is declared through `has_status(...,
known_defect_status=HTTPStatus.INTERNAL_SERVER_ERROR)` together with a strict
`xfail` limited to `KnownSandboxDefectError`. The test still explicitly expects
404; other failures remain unexpected. Unit tests exercise this assertion
policy directly, without importing or executing API test functions.

## Test-data generation

Test data follows three different rules:

1. Framework unit tests use small deterministic examples. Exact values make
   serialization, parsing, redaction, and validation failures reproducible.
2. UI and API lifecycle tests keep a deterministic payload shape but add a
   UUID-based suffix to resource identities. This prevents collisions in the
   shared public sandbox while preserving debuggability.
3. Negative tests start from valid data and change only the field relevant to
   the validation under test.

Faker is not currently a dependency because realistic names and addresses do
not exercise any additional Restful Booker rule. It becomes appropriate when
the system has locale-sensitive fields, broad equivalence classes, or enough
domain attributes that hand-written factories become expensive. In that case,
generation must be seeded for reproducible unit tests, while external resource
identities must still be unique per run.

## Failure and isolation rules

- Keep HTTP sessions function-scoped, including administrator authentication.
- Register unique resource identities before every API creation attempt,
  including negative tests; registration is not an assertion that creation succeeds.
- Preserve pytest's separate setup/call/teardown reports. Cleanup failures remain
  visible without replacing the original test assertion.
- Restrict a known-defect `xfail` to `KnownSandboxDefectError`, raised only when
  the documented server status is observed. Keep strict XPASS enabled.
- Diagnostic screenshots are best effort and bounded. Browser capture errors
  must not cause a second test failure.
- Run lint, formatting, typing, unit tests, then affected API/UI scenarios before
  a full regression run. Preserve existing expected results during refactoring.

## Adding a scenario

Choose the matching API/UI module and use its existing typed data and object
fixtures. Declare the layer (`api` or `ui`) and selection (`smoke` or `regression`)
markers, add Allure behavior metadata, then write preparation, action, and domain
assertion in that order. For a mutation, register the resource before the action;
for a UI prerequisite, compose API setup in a fixture. Use `pytest --collect-only`
to check discovery and run the scenario independently before the entire module.
