# UI Test Plan — Milestone 1

## Scope

Nine UI scenarios running against `https://automationintesting.online`.

## Home page

1. Display seeded rooms and open the selected room.
2. Validate required contact form values.
3. Submit a valid contact message and show confirmation.

## Reservation page

1. Display details and facilities for the selected room.
2. Recalculate the price summary for a selected stay period.
3. Validate guest details before a reservation is submitted.

## Administration area

1. Reject invalid administrator credentials.
2. Authenticate with valid administrator credentials.
3. Log out and prevent access to the authenticated state.

## Out of scope

- API tests and API clients
- destructive administration scenarios
- cross-browser matrix
- visual regression testing
- mobile viewport testing

These items may be added after the nine Chromium scenarios are stable.
