# 08 Wave 1 Hotel Spec

## Scope

- Property master
- Room type and room inventory
- Reservation lifecycle
- Check-in and check-out
- Housekeeping
- Maintenance
- Meal plans
- Staff and shifts
- Billing and folios

## Canonical Rule

Hotel exists as one unified pack. The legacy split between generic hotel routes
and travel hotel routes is explicitly retired.

## Legacy Risk To Eliminate

- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/hotel/*`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/travel/hotel/*`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/runtime-collections.ts`

## Enterprise Additions

- Room status integrity checks
- Inventory calendar with blocked and sold units
- Operational views for housekeeping and maintenance
- Direct booking support through publishing contracts

## Current Build Status

As of April 1, 2026, the canonical repo now contains the expanded hotel
foundation:

- SQL-backed hotel property, room type, room, reservation, housekeeping, and maintenance entities
- Reservation lifecycle transitions for pending, reserved, checked-in, checked-out, cancelled, and no-show
- Automatic housekeeping task creation on checkout
- Room-status integrity updates across housekeeping and maintenance flows
- Inventory summary endpoint for room-type availability snapshots
- Meal plan APIs and persistence
- Guest profile APIs and persistence
- Rate plan APIs with weekend and seasonal override support
- Availability rule APIs with stay restrictions and blackout dates
- Reservation-linked folios with auto-created base charges
- Folio charge posting for add-ons and incidentals
- Payment posting, balance tracking, folio close, and invoice issuance
- Refund posting against payments with folio balance recalculation
- Staff member and shift APIs
- Staff-backed assignment references for housekeeping and maintenance
- Night audit reports with blocker detection
- Automatic stay records on check-in plus room-move history
- Guest document metadata for KYC/compliance workflows
- Mongo-backed property profile, amenity catalog, and nearby-place content
- Summary reporting endpoint for operational and revenue snapshots
- External hotel Mongo adapter plan exposed for migration prep
- Reservations can now be created before room assignment and assigned later
- Room entities now track occupancy, housekeeping, and sell-state separately while keeping legacy status compatibility

This is the first real replacement for the legacy split hotel implementations.
The remaining work is now mostly advanced hardening: tax and settlement rules,
attendance analytics, full import execution and dry-run reconciliation, and
deeper reporting depth for enterprise finance and long-stay variants.

## Seed-Driven Expansion

The provided Mongo sample seed in `/Users/apple/Downloads/seed-data.js` is
broader than the current canonical PMS slice. It includes:

- hotel profile settings
- amenity taxonomy
- rich room-type merchandising
- meal plans
- guest profile details
- pricing and availability rules
- staff roster
- nearby discovery content

The detailed extension and migration plan is captured in
`/Users/apple/Desktop/WORK/GIT/kalpzero-enterprise/docs/13_HOTEL_ENTERPRISE_EXPANSION_PLAN.md`.
