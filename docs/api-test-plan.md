# API Test Plan

## Scope

Twenty-six external API scenarios running through the same `/api/*` contracts used
by the Restful Booker Platform UI.

## Authentication service

1. Return a token that matches the login response schema.
2. Reject invalid administrator credentials.
3. Accept a freshly issued token during validation.
4. Reject an unknown authentication token.

## Room service

1. Return a room collection matching the room schema.
2. Create and discover an isolated administrator-owned room.
3. Reject anonymous room creation.
4. Retrieve a created room through its canonical resource URL.
5. Reject anonymous room deletion.
6. Exclude a booked room from a matching date availability search.
7. Return `404 Not Found` for an unknown identifier.

## Booking service

1. Create and discover a booking for an isolated room.
2. Reject invalid guest fields.
3. Reject checkout before check-in.
4. Prevent anonymous access to room booking administration.
5. Retrieve a created booking as an administrator.
6. Prevent anonymous access to an individual booking.
7. Reject an overlapping booking for the same room.

## Message service

1. Create and discover a contact message.
2. Reject a malformed contact email.
3. Prevent anonymous message deletion.
4. Allow an administrator to mark a message as read.
5. Return `404 Not Found` for an unknown identifier.

## Branding service

1. Return branding and contact information matching the public schema.

## Report service

1. Return an empty, schema-valid availability report for a newly created room.
2. Show a created booking as an unavailable room period.

## Contract strategy

The suite uses `jsonschema` with Draft 2020-12 contracts. JSON Schema validates
response shape, required fields, primitive types, formats, and unexpected
properties. Domain assertion objects separately verify business meaning so a
schema-valid but incorrect response still fails.

## Resource lifecycle

Mutating tests create uniquely named rooms, bookings, and messages. The resource
lifecycle records a unique identity before each request, then stores
the identifier after discovery. If discovery or DTO parsing fails, cleanup can
still rediscover the resource. Resources are removed in reverse creation order:

```text
create room
  -> create booking
    -> execute test
  -> delete booking
-> delete room
```

Only resources registered by the current test are deleted. API create scenarios
perform the mutation explicitly in the test body; fixtures use the same
lifecycle when creation is only a prerequisite. Tests do not depend on execution
order or shared seeded identifiers.

## Known defects

Strict `xfail` scenarios document that the shared sandbox currently responds
with `500 Internal Server Error` for unknown room and message identifiers
instead of the expected `404 Not Found`. `strict=True` makes an unexpected fix
fail CI so the marker and defect documentation cannot become stale silently.
