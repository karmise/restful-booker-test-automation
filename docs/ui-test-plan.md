# UI Test Plan

## Scope

Fifteen UI scenarios running against `https://automationintesting.online`.

## Home page

1. Display a stable public catalogue room and open it by its canonical identifier.
2. Validate required contact form values.
3. Navigate to the contact section from the primary navigation.
4. Validate malformed email and phone values in the contact form.
5. Submit a valid contact message and show confirmation.

## Reservation page

1. Display details and facilities for the selected room.
2. Recalculate the price summary for a selected stay period.
3. Validate guest details before a reservation is submitted.
4. Cancel guest-details entry and return to date selection.
5. Validate malformed guest email and phone values.

## Administration area

1. Reject invalid administrator credentials.
2. Authenticate with valid administrator credentials.
3. Redirect an anonymous user away from protected room administration.
4. Open the authenticated booking report.
5. Log out and prevent access to the authenticated state.

## Out of scope

- API contract assertions inside UI scenarios
- destructive administration scenarios
- visual regression testing
- mobile viewport testing

API clients are allowed only in UI fixtures for controlled setup and teardown.
The browser-test bodies remain UI-only. Visual and mobile coverage may be added
after the functional scenarios remain stable across the CI browser matrix.
