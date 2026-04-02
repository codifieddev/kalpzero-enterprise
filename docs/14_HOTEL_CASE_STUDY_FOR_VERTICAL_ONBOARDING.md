# 14 Hotel Case Study For Vertical Onboarding

## Why Hotel Goes First

Hotel is the strongest Wave 1 case study because it forced the platform to
solve nearly every core enterprise pattern in one vertical:

- master data
- inventory and availability
- lifecycle transitions
- operations and assignments
- finance closure
- auditability
- public publishing hooks
- import-readiness

If KalpZero can onboard and run hotel cleanly, the same platform shape can be
reused for other business types with less ambiguity.

## Reusable Vertical Pattern

The hotel implementation now provides the canonical vertical pattern:

1. `master data`
Property, room type, meal plan, staff member.

2. `inventory or capacity`
Rooms, availability rules, room-state controls.

3. `transaction lifecycle`
Reservation from pending through terminal state.

4. `operational work`
Housekeeping, maintenance, shifts, staff assignment.

5. `finance closure`
Folio, charges, payments, refunds, invoice, night audit.

6. `public surface`
Publishing routes, discovery hooks, SEO pages.

7. `migration`
Source mapping, dry-run validation, canonical write, audit trail.

This is the model future business types should follow.

## Mapping Hotel To Other Business Types

### eCommerce

- master data: categories, products, variants
- inventory: stock and sellable quantity
- lifecycle: cart, order, payment, fulfillment, return
- operations: pick-pack-ship and warehouse tasks
- finance closure: order ledger, refunds, tax, invoice
- public surface: storefront and SEO catalog

### Tour & Travels

- master data: packages, suppliers, departures
- inventory: seats and departure capacity
- lifecycle: lead, quote, booking, traveler confirmation
- operations: vendor coordination and itinerary tasks
- finance closure: booking ledger, deposits, balance, refund, voucher
- public surface: package landing pages and discovery

### Real Estate

- master data: projects, properties, units, brokers
- inventory: unit availability and holds
- lifecycle: lead, visit, offer, booking, agreement
- operations: broker follow-up, document verification, site visits
- finance closure: booking ledger, payment plan, receipt, refund
- public surface: listings and locality discovery

### LMS / School

- master data: courses, classes, teachers, students
- inventory: seats, timetable, classroom capacity
- lifecycle: admission, enrollment, attendance, assessment, completion
- operations: faculty assignment, scheduling, parent communication
- finance closure: fees, dues, refunds, receipts
- public surface: admissions and course pages

### Clinic / Doctor

- master data: doctors, services, patients, departments
- inventory: appointment slots and room availability
- lifecycle: appointment, consultation, follow-up
- operations: nurse workflow, lab coordination, document handling
- finance closure: encounter ledger, payment, refund, invoice
- public surface: doctor profile, service pages, booking pages

## Onboarding Rule For New Verticals

Do not onboard a new business type from custom pages or ad hoc CRUD alone.
Use the hotel case study as the readiness checklist:

- canonical master entities exist
- lifecycle states are explicit
- operations and assignments are modeled
- finance closure exists
- audit events exist
- public blueprint exists
- import adapter exists
- dry-run migration exists
- tests cover the main lifecycle

If a vertical does not satisfy those conditions, it is not onboarding-ready.

## Immediate Use In KalpZero

The hotel case study should now guide the next vertical work:

1. close the remaining hotel stabilization and hardening backlog
2. align commerce order closure, inventory operations, and refunds to the same
   pattern
3. run the first backend onboarding pilot on hotel and commerce only
4. move to travel after commerce reaches the same onboarding-readiness bar
