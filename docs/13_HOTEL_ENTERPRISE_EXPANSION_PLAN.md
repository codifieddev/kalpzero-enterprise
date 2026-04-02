# 13 Hotel Enterprise Expansion Plan

## Objective

Use the current canonical hotel pack as the operational core, then extend it
into a full hotel and rent-accommodation system without breaking the existing
property, room, reservation, housekeeping, and maintenance flows.

The reference input for this plan is:

- current canonical hotel implementation in
  `/Users/apple/Desktop/WORK/GIT/kalpzero-enterprise/apps/api/app/services/hotel.py`
- provided Mongo sample seed in `/Users/apple/Downloads/seed-data.js`

## What The Seed Data Proves

The sample data is not a small booking demo. It already models a realistic
hotel business surface with:

- hotel profile and public-facing property settings
- amenity categories and amenity master data
- rich room-type catalog with merchandising data
- physical room inventory and operational room state
- meal plans
- guest/customer data with loyalty and identity fields
- historical, in-house, and future bookings
- housekeeping and maintenance tasks
- staff roster
- pricing rules, weekend pricing, seasonal pricing, and availability policy
- nearby places and public discovery content

This means the current canonical hotel slice is directionally correct, but it
is still only the PMS core. The seed model expects a much broader system.

## Current Canonical Coverage

Already implemented:

- property master
- room type master
- room inventory
- reservation lifecycle
- room availability summary
- housekeeping task flow
- maintenance ticket flow
- meal plans
- guest profile extension
- guest document metadata
- stays and room moves
- rate plans
- availability rules and stay restrictions
- folios, charge lines, payment posting, and invoice issuance
- refunds
- staff members and shifts
- staff-backed assignment references for housekeeping and maintenance
- night audit
- property profile docs, amenity catalogs, and nearby-place docs
- summary reporting
- external hotel import plan exposure
- audit and outbox events

Currently missing or incomplete:

- full hotel profile richness like geo coordinates and richer policy structures
- deeper room-type merchandising and media management
- secure KYC upload and verification workflows beyond document metadata
- unassigned bookings at room-type level
- guaranteed and confirmed reservation states beyond the current lifecycle
- settlement controls, tax profiles, and deeper night-audit closing rules
- deeper rate management including derived pricing strategies and negotiated rates
- attendance and workforce analytics
- full import execution and dry-run reconciliation against the seed source
- rent-style extension for apartments, villas, hostels, serviced stays, and co-living

## Critical Model Corrections

### 1. Room status is overloaded

The current model stores a single `room.status`. The seed data shows at least
three different concerns:

- occupancy state: vacant, occupied
- housekeeping state: clean, dirty, inspected, dnd
- sell state: sellable, blocked, maintenance, out_of_order

These should not remain one field. The full system should split them into
explicit fields so operations, front desk, and revenue logic do not conflict.

### 2. Reservations require room assignment too early

The current reservation model requires `room_id` at creation time. The seed
bookings allow future bookings with `roomNumber: null`, which is correct for
normal hotel operations.

The full system must support:

- reservation against room type only
- later room assignment
- pre-arrival upgrade or room move
- walk-in immediate assignment

### 3. Booking statuses are too narrow

Current statuses are only:

- `reserved`
- `checked_in`
- `checked_out`
- `cancelled`

The seed requires a broader lifecycle:

- `pending`
- `confirmed`
- `checked_in`
- `checked_out`
- `cancelled`
- `no_show`

For enterprise use, a richer lifecycle should exist:

- `draft`
- `pending`
- `confirmed`
- `guaranteed`
- `checked_in`
- `checked_out`
- `cancelled`
- `no_show`

### 4. Pricing and availability must not stay as disconnected docs

The seed has `pricing`, `pricing_rules`, and `availability` as separate Mongo
collections. That is useful as a source system, but not as the final canonical
truth.

The canonical system should treat them as:

- rate plans and seasonal overrides in SQL
- availability rules and restrictions in SQL
- snapshots and public materializations in Mongo when needed

The current canonical repo now covers the first part of that correction with:

- rate plan APIs in SQL
- weekend pricing support
- seasonal override support
- availability rules in SQL
- minimum and maximum stay restrictions
- blackout date support
- reservation-linked folios in SQL
- payment posting in SQL
- refund posting in SQL
- invoice issuance from the folio layer
- stay records and room-move history in SQL
- guest-document metadata in SQL

### 5. The source data has an identity mismatch

In the seed, `pricing.roomId` and `availability.roomId` refer to values like
`rm1`, `rm2`, and `rm3`, which are room-type ids, not physical room inventory
ids. The import layer must correct that by mapping those fields to
`room_type_id`.

## Full Hotel System Blueprint

### A. Property and Brand Management

Keep the current `hotel_property` entity, but extend it with:

- property kind: hotel, resort, villa, serviced_apartment, hostel, holiday_home, co_living
- short description and long description
- full address and geo coordinates
- check-in and check-out policy
- star rating
- contact number, email, website
- tax and invoice settings
- banking and settlement settings
- brand media and gallery hooks

### B. Room Type and Inventory

Extend room types with:

- category
- bed type
- room size
- view
- smoking policy
- balcony flag
- theme
- soundproofing level
- workspace flag
- bathroom type
- extra bed price
- refundable flag
- amenity ids
- image gallery

Extend rooms with:

- inventory code
- active flag
- floor
- operational notes
- feature tags
- last cleaned timestamp
- occupancy status
- housekeeping status
- sell status

### C. Reservations, Stay Operations, and Front Desk

Reservations must support:

- room-type hold before room assignment
- booking reference
- booking source
- primary guest and co-guests
- guest notes and special requests
- early check-in and late check-out flags
- actual check-in and check-out timestamps
- no-show handling
- room assignment and reassignment
- upgrades and room moves

Add a separate stay layer:

- stay record for the in-house lifecycle
- keycard issue tracking
- incident log
- room move history

### D. Guest CRM and Identity

Use the shared `Customer` as the cross-platform person record, then add a hotel
guest extension for:

- loyalty tier
- VIP flag
- preferred room or room type
- dietary preference
- company or corporate account
- local ID or passport fields
- uploaded KYC documents
- guest preferences and service notes

### E. Revenue, Rate, and Availability Management

Add these canonical modules:

- meal plans
- rate plans
- seasonal pricing
- weekend pricing
- discount and surcharge rules
- minimum stay and maximum stay restrictions
- blackout dates
- occupancy-based pricing
- corporate and negotiated rates

This should support both hotel and rent-style use cases.

### F. Billing, Folio, and Payments

The current hotel slice has only reservation totals. The full system needs:

- folio header
- folio charge lines
- room revenue
- meal plan revenue
- taxes and fees
- add-ons and incidentals
- payment records
- refund records
- invoice or receipt generation
- night audit support

### G. Operations

The housekeeping and maintenance core already exists, but needs to expand with:

- room inspection outcomes
- DND state
- out-of-order and out-of-service handling
- recurring preventive maintenance
- maintenance cost estimates and comments
- SLA and escalation state
- assignment by staff member, not plain text only

### H. Staff and Workforce

Add a staff subsystem for:

- employee master
- department
- role
- shift
- attendance
- emergency contact
- active or inactive state
- task assignment to housekeeping and maintenance

### I. Public Experience and Discovery

The seed includes `hotel_settings`, `amenities`, and `nearby`. These should
feed Mongo-backed runtime documents for:

- public property profile
- room-type presentation
- nearby places
- amenity presentation
- booking and inquiry pages
- SEO and discovery cards

### J. Rent-Based Extension

To support rent-based accommodations without replacing the hotel pack, extend
the property with `property_kind` and the inventory with `stay_mode`:

- nightly
- weekly
- monthly
- mixed

This allows the same platform to support:

- serviced apartments
- villas
- hostels
- co-living
- managed rentals

without forcing a separate architecture.

## Canonical Storage Plan

### SQL Source Of Truth

Use SQL for:

- properties
- room types
- rooms
- reservations
- stays
- folios and charge lines
- meal plans
- rate plans and pricing rules
- availability restrictions
- housekeeping tasks
- maintenance tickets
- staff records and shifts
- payment records

### Mongo Runtime Documents

Use Mongo for:

- property profile and public content
- amenity category presentation
- media galleries
- nearby places
- public room-type content
- rich policy documents
- discovery materializations

## Source Collection To Canonical Mapping

| Source collection | Canonical target | Notes |
| --- | --- | --- |
| `hotel_settings` | `hotel.property_profile_doc` | public profile and operating policy |
| `amenity_categories` | `hotel.amenity_category` | master reference |
| `amenities` | `hotel.amenity_catalog_doc` | category plus nested amenity presentation |
| `room_types` | `hotel.room_type` | rich room-type master |
| `rooms` | `hotel.room` | physical inventory |
| `meal_plans` | `hotel.meal_plan` | rate inclusion logic |
| `customers` | `customer` + `hotel.guest_profile` | shared person plus hotel extension |
| `bookings` | `hotel.reservation` + `hotel.stay` | future bookings and in-house stays |
| `housekeeping` | `hotel.housekeeping_task` | operational tasks |
| `maintenance` | `hotel.maintenance_ticket` | engineering workflow |
| `pricing_rules` | `hotel.rate_rule` | pricing logic |
| `staff` | `hotel.staff_member` | workforce |
| `pricing` | `hotel.rate_plan` | weekend and seasonal price overrides |
| `availability` | `hotel.availability_rule` | min/max stay and blackout rules |
| `nearby` | `publishing.nearby_place_doc` | public discovery content |

## What Must Change In The Current Hotel Pack

### Keep

- property, room type, room, reservation, housekeeping, maintenance tables
- reservation conflict logic
- room-status integrity behavior
- housekeeping auto-creation on checkout
- audit and outbox patterns

### Extend

- property model with hotel profile and policy fields
- room type with amenity and merchandising fields
- room model with split operational status fields
- reservation model with booking reference, source, lifecycle expansion, room assignment nullable, meal plan, special requests, actual timestamps
- guest extension model
- rate, availability, folio, payment, staff, and nearby content models

### Remove Or Avoid

- avoid keeping price and availability as isolated unversioned Mongo collections
- avoid using one `room.status` field for occupancy, housekeeping, and sellability
- avoid forcing room assignment at reservation creation time
- avoid duplicating customer truth between hotel-only and platform-wide models

## Recommended Delivery Order

### Phase 1: Strengthen the current PMS core

- expand property, room type, room, and reservation contracts
- add nullable room assignment
- add richer reservation statuses
- add meal plans
- add guest profile extension

### Phase 2: Revenue and availability

- rate plans
- seasonal pricing
- restrictions and blackout rules
- availability engine
- folio and payment records

### Phase 3: Operations and workforce

- staff master
- shift and attendance
- richer housekeeping and maintenance assignment
- inspection and out-of-order flow

### Phase 4: Public and discovery

- property profile docs
- nearby docs
- amenity-driven public blocks
- room-type marketing blocks

### Phase 5: Rent-mode extension

- monthly stay support
- deposit handling
- long-stay billing
- unit-based availability for serviced apartments and rentals

## Immediate Build Recommendation

Before onboarding a real hotel business, the next implementation steps should
be:

1. add rate plans and availability restrictions
2. add folio, payment, and invoice layers
3. add staff, shifts, and assignment references
4. add property profile docs, amenities, and nearby public content
5. import this Mongo seed model through a formal adapter and dry-run report

That path keeps the current system in place while moving it toward a full
enterprise hotel system.
