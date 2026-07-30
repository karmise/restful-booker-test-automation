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

## Constants

A value is extracted only when its name explains domain meaning or when the
same contract value is reused:

- environment keys and shared DTO examples may be private module constants;
- protocol and business constants owned by production code stay in the
  production module;
- one-off expected values remain inside the test that documents them;
- tests do not import a production constant merely to assert that same
  constant, because that would make the check tautological.

There is intentionally no global `test_constants.py`. A global constants file
would couple unrelated suites and make expected behavior harder to read.

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
