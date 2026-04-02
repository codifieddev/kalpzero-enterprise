# 18 Backend Onboarding Pilot Plan

## Current Pilot Scope

As of April 2, 2026, backend onboarding is intentionally limited to:

- `hotel`
- `commerce`

Travel remains implemented, but it is not yet approved for business onboarding.

## Why The Pilot Scope Is Narrow

The platform now has enough depth to validate real onboarding only where the
full operating loop is mostly in place:

- master data
- transactional lifecycle
- operational controls
- finance closure
- audit and outbox coverage

Hotel satisfies that bar most strongly. Commerce is now close enough after the
addition of pricing, tax, payments, refunds, invoice issuance, warehouse stock,
and fulfillment operations.

## Pilot Goals

The pilot should prove:

- tenant provisioning works against the hybrid storage model
- registry and permission surfaces are pack-driven and fail closed
- blueprint and theme assignment can be attached at tenant creation time
- hotel and commerce lifecycle operations work end to end
- finance closure is explicit and auditable
- import dry-run setup is traceable before real source execution

## Pilot Flow

1. Create or verify agency and tenant via `/platform/agencies` and
   `/platform/tenants`.
2. Inspect `/platform/onboarding-readiness` before tenant creation.
3. Confirm `/platform/registry` returns the expected modules:
   `commerce.catalog`, `commerce.inventory`, `commerce.orders`,
   `commerce.fulfillment`, `commerce.finance`,
   `hotel.properties`, `hotel.inventory`, `hotel.reservations`,
   `hotel.operations`.
4. Assign the tenant blueprint and public runtime configuration.
5. Seed or import canonical test data through the approved API surfaces.
6. Run one hotel and one commerce end-to-end workflow.
7. Inspect audit and outbox traces for each privileged operation.

## Minimum Commerce Scenario

- create category
- create product and variant
- create warehouse and opening stock
- create tax profile, price list, and coupon
- place order
- create fulfillment
- create shipment
- capture payment
- issue invoice
- record refund

## Minimum Hotel Scenario

- create property, room types, and rooms
- create reservation
- record folio charges
- record payment
- issue invoice
- run refund and nightly summary checks

## Exit Criteria

Pilot onboarding is successful only if:

- no tenant provisioning blockers appear in production-grade infra
- registry and permissions match the selected packs
- commerce and hotel finance states reconcile correctly
- commerce stock, fulfillment, and shipment traces reconcile correctly
- audit and outbox records exist for tenant provisioning and finance actions
- no fallback or demo behavior contaminates tenant runtime data
