---
name: add-api-test
description: Add or change a Restful Booker API scenario in tests/api through the framework's layers (client, DTO, schema, contract, assertion object, fixture, test). Use when asked to cover a new endpoint, status code, validation rule, or response contract. Not for UI tests or framework unit tests.
---

# Add an API scenario

## 1. Pin down the expectation before writing code

Write down, in one or two lines: endpoint and method, preconditions, the single
expected outcome, and where that expectation comes from (requirement, API
documentation, or an existing contract). If the source is missing or ambiguous,
ask. Never derive the expected value from what the sandbox currently returns.

## 2. Reuse before adding

Look for existing pieces, in this order, and reuse them:

| Need | Location |
| --- | --- |
| HTTP call | `src/restful_booker/api/clients/<service>_client.py` |
| Request/response shape | `src/restful_booker/api/dto/` |
| JSON Schema | `src/restful_booker/api/schemas/<name>.json` |
| Expected text | `src/restful_booker/contracts/api/<service>.py` |
| Domain check | `src/restful_booker/api/assertions/` |
| Test data | `ApiTestDataFactory` in `src/restful_booker/api/testdata.py` |
| Preconditions | `fixtures/api/` (`created_room`, `created_booking`, ...) |

## 3. Add missing layers bottom-up

Client method with `@report_step` (returns the raw `Response`, never asserts) →
DTO → schema → contract constant (`Final`) → assertion method with a
business-language failure message → fixture if a precondition is reusable.
Register new fixtures in `tests/api/conftest.py`.

## 4. Write the test

- Module `pytestmark` already has the Allure suite/feature; add `@pytest.mark.api`,
  `smoke` or `regression`, `@allure.story`, `@allure.title`, `@allure.severity`.
- Body order: preparation, action, assertions. One path, one outcome. Use
  `parametrize` for different inputs with the same assertion shape.
- Before any mutating request, register the resource with
  `api_resource_lifecycle.track_room/track_booking/track_message`, also in
  negative tests.
- Every `has_status` call carries a `because=` explaining the business rule.
- A documented sandbox defect uses `known_defect_status=` plus a strict
  `xfail(raises=KnownSandboxDefectError)`; do not invent new known defects.

## 5. Verify, narrow to wide

```bash
poetry run ruff format . && poetry run ruff check . && poetry run mypy src fixtures tests
poetry run pytest --collect-only -q tests/api/<module>.py
poetry run pytest tests/api/<module>.py::<test_name>
poetry run pytest tests/api/<module>.py
poetry run pytest tests/unit
```

If the new test fails against the sandbox, do not change the expectation. Run
`qa.py triage allure-results` from qa-automation-agent, then report whether the
failure points to the product, the environment, or the new test.

## 6. Report

What was added (files and layers), the source of the expectation, the exact
commands run with their results, and anything not verified.
