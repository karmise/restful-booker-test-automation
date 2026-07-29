# API Test Plan

## Scope

Fifteen external API scenarios running through the same `/api/*` contracts used
by the Restful Booker Platform UI.

## Authentication service

1. Return a token that matches the login response schema.
2. Reject invalid administrator credentials.
3. Accept a freshly issued token during validation.

## Room service

1. Return a room collection matching the room schema.
2. Create and discover an isolated administrator-owned room.
3. Reject anonymous room creation.

## Booking service

1. Create and discover a booking for an isolated room.
2. Reject invalid guest fields.
3. Reject checkout before check-in.
4. Prevent anonymous access to room booking administration.

## Message service

1. Create and discover a contact message.
2. Reject a malformed contact email.
3. Prevent anonymous message deletion.

## Branding service

1. Return branding and contact information matching the public schema.

## Report service

1. Return an empty, schema-valid availability report for a newly created room.

## Contract strategy

The suite uses `jsonschema` with Draft 2020-12 contracts. JSON Schema validates
response shape, required fields, primitive types, formats, and unexpected
properties. Domain assertion objects separately verify business meaning so a
schema-valid but incorrect response still fails.

## Resource lifecycle

Mutating tests create uniquely named rooms, bookings, and messages. Function
fixtures discover the persisted resource identifier and register authenticated
cleanup. Pytest unwinds dependent fixtures in reverse order:

```text
create room
  -> create booking
    -> execute test
  -> delete booking
-> delete room
```

Only resources created by the current test are deleted. Tests do not depend on
execution order or shared seeded identifiers.
