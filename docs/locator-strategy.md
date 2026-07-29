# Locator Strategy

Locators are application contracts, not incidental DOM paths. The framework
uses the following order of preference:

1. Semantic role and accessible name for interactive elements.
2. Associated label for form controls.
3. Stable `data-testid` when semantics are unavailable or ambiguous.
4. User-visible text for stable content and assertions.
5. Short, scoped CSS for a component boundary that has no semantic contract.
6. XPath only as a documented exception.

## Rules

- Raw selectors stay inside page objects and components.
- Every action locator must resolve to one intended element.
- Repeated content is scoped to a business container before its child is found.
- Positional selectors such as `nth()` are avoided unless order is the behavior
  under test.
- Generated class names, deep CSS chains, and DOM ancestry XPath are prohibited.
- Playwright web-first assertions replace fixed sleeps.

## Current application contracts

The contact form exposes stable test IDs such as `ContactName` and
`ContactDescription`. The administration login form exposes associated labels
for Username and Password. Room cards have no semantic container or test ID, so
the page object uses the short `.room-card` component boundary and filters it by
the visible room name before locating its Book now link.

The contact form's Message label currently points to `message`, while the
textarea ID is `description`. The component therefore uses
`data-testid="ContactDescription"` instead of relying on the broken label
association.

