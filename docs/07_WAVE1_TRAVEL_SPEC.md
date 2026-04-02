# 07 Wave 1 Travel Spec

## Scope

- Package management
- Itinerary day modeling
- Departures and seat inventory
- Traveler records
- Lead capture and qualification
- Public package pages
- Quote-to-booking workflow

## Enterprise Additions

- Supplier references for hotels, activities, and transfers
- Departure-level pricing and availability
- Lead source analytics
- Operator tasking for itinerary and booking follow-up

## Legacy Reuse

- Travel package and itinerary concepts from
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/travel`
- Public trip presentation ideas from the current publishing surface

## Current Status On April 1, 2026

- Canonical SQL travel entities are implemented for packages, itinerary days,
  departures, and leads
- Travel API routes now exist for:
  - `/travel/overview`
  - `/travel/packages`
  - `/travel/departures`
  - `/travel/leads`
  - `/travel/legacy/plan`
- Audit and outbox coverage is implemented for package, departure, and lead
  operations
- Legacy adapter mapping is formalized in
  `/Users/apple/Desktop/WORK/GIT/kalpzero-enterprise/adapters/legacy-kalpzero/travel-packages.yaml`

## Direction Locked On April 2, 2026

Travel is now the selected next vertical after hotel.

This decision is based on:

- the legacy repo already containing a real travel package and supplier-catalog
  surface
- the canonical repo already containing the first half of the travel operating
  model
- the hotel case study proving the exact extension pattern travel now needs:
  lifecycle completion, operations, finance closure, public depth, and
  migration execution

## Remaining Wave 1 Work

- Traveler records beyond lead capture
- Quote-to-booking conversion and seat decrement workflow
- Richer travel-specific public package blocks beyond the first live package
  materialization in the blueprint runtime
- Supplier catalog sync for hotels, activities, and transfers
- Booking finance closure:
  deposits, balance dues, refunds, invoices, and vouchers
- Operator workflow:
  supplier confirmation, manifest preparation, and departure tasking
