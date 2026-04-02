# 06 Wave 1 Commerce Spec

## Scope

- Product catalog
- Categories and attributes
- Variants and pricing
- Coupons
- Orders
- Payment abstraction
- Fulfillment and shipment hooks
- Public storefront publishing

## Enterprise Additions

- B2B and retail price lists
- Tax contract layer
- Multi-warehouse extension point
- Catalog import and inventory sync adapters
- Audit and approval for sensitive price changes

## Legacy Reuse

- Product and category concepts from the current repo
- Builder and SEO ideas from the existing public product surfaces

## Non-Reuse

- Do not allow commerce structures to become the hidden schema for real estate,
  travel, or hotel

## Current Build Status

As of March 31, 2026, the canonical repo now contains the first persisted
commerce slice:

- SQL-backed categories, products, variants, orders, and order lines
- Catalog creation routes with variant-level inventory
- Order creation and status transitions with inventory reservation and restore logic
- Tax profiles, price lists, and coupon masters
- Order pricing with price-list overrides, coupon discounts, and tax calculation
- Payment capture, refunds, and invoice issuance
- Warehouse masters, stock adjustments, stock ledger, and low-stock visibility
- Fulfillment creation, packing, shipment creation, and delivery confirmation
- Outbox emission for `commerce.order.created`
- A concrete legacy commerce adapter plan for products, variants, categories, and orders

## Direction Locked On April 2, 2026

Commerce is now the prioritized vertical after hotel stabilization.

The reason is not that travel is weak. The reason is that commerce provides the
broadest reusable business foundation for backend onboarding across multiple
customer types.

The first reusable catalog-taxonomy slice is now implemented in the backend:

- commerce brands
- commerce vendors
- commerce collections
- commerce attributes
- commerce attribute sets
- product-level attribute values
- variant-level attribute values

This is intentionally designed as the first shared attribute pattern that later
verticals can follow, rather than as one-off ecommerce-only metadata.

## Extended Commerce Target

Commerce now needs to be completed to the same standard hotel established:

- master data:
  brands, vendors, collections, category hierarchy, attributes, media bindings
- inventory:
  warehouses, stock ledger, reservation rules, transfers, low-stock controls
- lifecycle:
  cart, checkout, payment, order, fulfillment, return, exchange, cancellation
- operations:
  pick-pack-ship, shipping methods, carrier hooks, warehouse tasking
- finance closure:
  coupons, price lists, tax profiles, refunds, invoices, settlements, credit notes
- public surface:
  storefront blocks, search, merchandising, SEO, discovery materialization
- migration:
  dry-run import, reconciliation, and external catalog adapters

## Implemented Operations Layer

Commerce now also includes:

- warehouse masters with default-warehouse assignment
- per-warehouse stock records with on-hand, reserved, and available quantities
- stock ledger entries for restock, reservation, release, and fulfillment
- fulfillment creation with line-level quantities
- packing transitions, shipment creation, and delivery confirmation

That means the commerce pack now covers the main inventory-to-operations loop
instead of stopping at priced order creation.

## Immediate Remaining Work

- returns, exchanges, settlement controls, and credit-note depth
- storefront blueprint runtime and public discovery depth
- import execution and dry-run reconciliation

## Implemented Governance Layer

The catalog-governance layer now includes:

- brands and vendor master data
- merchandised collections
- product linkage to brand, vendor, and collections
- reusable attribute definitions and grouped attribute sets
- validated product and variant attribute assignments

This means the commerce core is no longer only `category -> product -> variant`.
It now has the first governed catalog structure needed for broader business
onboarding.

## Implemented Pricing Layer

The pricing layer now includes:

- reusable tax profiles with explicit rule sets
- customer-segment price lists with per-variant overrides
- scoped coupons with subtotal thresholds and optional caps
- order pricing that resolves base price, discount, tax, and final total

This means the commerce order model now carries explicit `subtotal`, `discount`,
`tax`, and `total` values instead of relying on a single opaque total field.

## Implemented Finance Closure

Commerce now also includes:

- payment recording with explicit capture and authorization states
- refund recording against captured payments with refundable-balance validation
- invoice issuance against fully paid orders
- order-level finance state with `payment_status`, `paid`, `refunded`, and
  `balance` values

That moves commerce much closer to the same closure standard that hotel already
established.
