# UI Test Plan

## Scope

Fifteen UI scenarios running against `https://automationintesting.online`.

## Home page

1. Display seeded rooms and open the selected room.
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

- API tests and API clients
- destructive administration scenarios
- cross-browser matrix
- visual regression testing
- mobile viewport testing

These items may be added after the 15 Chromium scenarios are stable.
