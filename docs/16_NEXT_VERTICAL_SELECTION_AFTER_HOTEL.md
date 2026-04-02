# 16 Next Vertical Selection After Hotel

## Decision

Hotel should be stabilized first, then commerce is the next vertical that
should be onboarded using the hotel case study as the canonical template.

Travel moves behind commerce. Real estate stays blocked until it becomes a true
domain model instead of a filtered commerce facade.

## Why Commerce Is The Correct Next Step

Commerce is the best next onboarding target for platform leverage, even though
travel is still a strong later candidate.

The reason is business coverage. A stronger commerce core can be reused across
many customer types:

- direct-to-consumer retail
- catalog-led businesses
- B2B order taking
- productized services with checkout
- add-on sales for hotel, travel, clinic, school, and other future verticals

That makes commerce the better backend onboarding pilot after hotel.

In the legacy repo, commerce already has:

- dedicated product CRUD in
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/ecommerce/products/route.ts`
- order lifecycle endpoints in
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/ecommerce/orders/route.ts`
- public product delivery and storefront SEO concepts under
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/public/product`
  and `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/(public)/product-page`

In the canonical repo, commerce already has:

- master data
- sellable inventory
- early lifecycle
- audit and outbox events
- public surface
- migration baseline

What is missing is the second half:

- checkout and payment contracts
- returns and exchanges
- fulfillment and warehouse operations
- finance closure
- richer public blocks

That is still a controlled extension from the hotel template, and it gives
KalpZero a broader onboarding base than travel does.

## Legacy Repo Validation

The legacy repo confirms the current direction is correct.

### Commerce

Commerce in legacy Kalp is a real reusable vertical:

- product and order APIs are mature enough to reuse concepts from:
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/ecommerce/products/route.ts`
  and
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/ecommerce/orders/route.ts`
- public storefront and SEO work are well represented in the old repo
- commerce is common enough to support many business types without forcing a
  new domain immediately
- the missing parts are operational and finance completion, not category
  confusion

Commerce is the best next onboarding target because it strengthens the broadest
shared business surface.

### Travel

Travel in legacy Kalp is still a real vertical, even if incomplete:

- `travel_packages` has dedicated CRUD and normalization.
- public package exposure exists separately from admin CRUD.
- supplier references already exist as hotel/activity/transfer catalogs.
- travel also contains an older hotel-management branch, which proves the
  product direction but must not be reused as canonical runtime because it
  duplicates hotel schema again.

Travel remains valid, but it should come after commerce because backend
onboarding benefits more from a common order/catalog stack than from deeper
travel operations first.

### Real Estate

Real estate is not ready for onboarding:

- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/(dashboard)/real-estate/page.tsx`
  explicitly reuses `/api/ecommerce/products?type=property`
- that means listings are still commerce products with property vocabulary
- there is no true unit inventory, site-visit lifecycle, broker workflow,
  booking ledger, or agreement model

Real estate should not be the next canonical vertical.

## Comparison Against The Hotel Template

| Vertical | Master Data | Inventory / Capacity | Lifecycle | Operations | Finance Closure | Public Surface | Migration Reuse | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commerce | Strong | Medium | Medium | Weak | Medium | Strong | Strong | Next |
| Travel | Strong | Strong | Medium | Medium | Weak | Medium | Strong | After Commerce |
| Real Estate | Weak | Weak | Weak | Weak | Weak | Medium | Weak | Blocked |

## What To Reuse From Legacy Commerce

- product and category contracts
- public product and storefront SEO patterns
- order and customer linkage ideas
- builder patterns that fit storefront pages

## What Not To Reuse From Legacy Commerce

- direct Mongo collection shapes as canonical truth
- any reuse of commerce schemas as hidden substitutes for real estate, hotel, or
  travel
- legacy assumptions that storefront CRUD alone is enough for onboarding-ready
  commerce

## Commerce Should Now Match The Hotel Checklist

Commerce is not onboarding-ready until it satisfies the same checklist hotel now
uses:

- canonical master entities exist
- inventory and reservation controls are explicit
- lifecycle states are explicit
- operator tasks and assignments exist
- finance closure exists
- audit and outbox events exist
- public blueprint exists
- import adapter exists
- dry-run migration exists
- tests cover the main lifecycle

## Immediate Build Order For Commerce

1. Stabilize hotel hardening gaps needed for pilot confidence.
2. Add price lists, coupons, tax profiles, and payment contracts.
3. Add fulfillment, shipment, warehouse, and stock-movement operations.
4. Add refunds, returns, exchanges, invoice, and settlement controls.
5. Add stronger storefront blueprint blocks and commerce discovery materialization.
6. Add dry-run import execution and reconciliation from legacy commerce sources.
7. Use hotel plus commerce as the first backend business onboarding pilot.

## What This Means For The Platform

The current architecture is on the right track.

Hotel proved the platform can support:

- transactional core data
- document-backed public content
- operational workflows
- finance closure
- auditability
- migration planning

Commerce is the best next proof that the same pattern can onboard another
business type at broader scale without collapsing back into generic CRUD.
