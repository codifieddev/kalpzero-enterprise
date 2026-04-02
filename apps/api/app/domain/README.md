# Domain Boundaries

Each folder under `app/domain` represents a bounded context for the canonical
platform:

- `platform`: tenancy, registry, plans, entitlements, audit
- `auth`: identity, SSO, session, and role assignment
- `commerce`: catalog, pricing, cart, order, tax, shipment
- `travel`: package, itinerary, departures, traveler, lead
- `hotel`: property, room inventory, reservation, check-in/out, housekeeping
- `ai`: provider governance, usage, knowledge ingestion, prompt boundaries
- `imports`: source registration, mapping, validation, import reporting
- `publishing`: domains, pages, SEO, public content lifecycle

Cross-domain writes should flow through service boundaries and an explicit
outbox/event model.
