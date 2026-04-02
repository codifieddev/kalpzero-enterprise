# 04 Canonical Data Model

## Shared Core

- `Agency`
- `Tenant`
- `User`
- `Membership`
- `Role`
- `Permission`
- `FeatureFlag`
- `BrandProfile`
- `DomainProfile`
- `Page`
- `MediaAsset`
- `Form`
- `FormResponse`
- `Customer`
- `Booking`
- `Invoice`
- `PaymentRecord`
- `ImportJob`
- `AuditEvent`
- `AiSession`

## Vertical Packs

- `commerce`: product, category, variant, cart, order, coupon, shipment, tax, payment
- `travel`: package, itinerary day, departure, traveler, lead, activity ref, transfer ref
- `hotel`: property, room type, room, inventory calendar, reservation, housekeeping, maintenance, meal plan, staff

## Storage Placement

- SQL source of truth: agencies, tenants, roles, permissions, audit events,
  import jobs, commerce orders, hotel reservations, and operational task records
- MongoDB runtime docs: pages, form payloads, AI knowledge, import staging,
  discovery materializations, and flexible tenant-specific document payloads
- Redis ops: cache, queues, worker coordination, and rate limits

## Canonical Rule

Do not use one generic `product` model to represent every business vertical.
Travel and hotel must have their own explicit domain entities. This directly
avoids the kind of schema drift visible in the legacy hotel implementation.
