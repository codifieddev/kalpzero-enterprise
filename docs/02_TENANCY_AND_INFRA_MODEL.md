# 02 Tenancy And Infra Model

## Tenancy Model

- Shared control plane stores agencies, tenants, memberships, plans, roles, and registry state
- Runtime data is tenant scoped by canonical identifiers
- Enterprise tenants can upgrade to dedicated database, storage, cache, and AI profiles

## Infra Profiles

- `shared`: default multi-tenant infra for standard customers
- `dedicated`: isolated data plane and secrets boundary for enterprise customers

## Onboarding Gate

Tenant provisioning is not allowed purely because the API is running. The
platform now checks onboarding readiness before creating a tenant.

- Only pilot-ready verticals can be onboarded: `commerce`, `hotel`
- Planned packs such as `real_estate`, `clinic`, `school`, `lms`, and
  `single_doctor` are intentionally blocked until their canonical domain packs
  are production ready
- `dedicated` tenants must include a `dedicated_profile_id`
- `shared` tenants must not include a `dedicated_profile_id`
- Non-test environments must use business-grade control-plane and runtime-doc
  infrastructure instead of SQLite or in-memory runtime-doc storage

The current readiness report is exposed from
`GET /platform/onboarding-readiness`.

As of April 2, 2026, the pilot-ready onboarding scope is intentionally narrower
than the broader Wave 1 build scope:

- pilot-ready now: `commerce`, `hotel`
- still implemented but not yet approved for onboarding: `travel`

The readiness report now also exposes per-vertical capability summaries so the
platform can explain why a pack is approved, in progress, or blocked.

## Storage Layers

- Control plane SQL stores agencies, tenants, auth, RBAC, audit, outbox, and
  transactional Wave 1 records
- Runtime MongoDB stores builder content, form payloads, AI knowledge, import
  staging, and denormalized discovery documents
- Redis stores worker queues, cache, rate limits, and operational coordination

Dedicated tenants can receive isolated Postgres, MongoDB, and Redis resources
under the same logical model.

As of April 2, 2026, runtime documents are provisioned with a per-tenant Mongo
database strategy. On tenant creation, the platform now:

- creates a tenant-scoped runtime database with the canonical collection set
- seeds the first business blueprint document
- seeds the initial public pages from the blueprint route map
- seeds the discovery document so the public runtime can render immediately

This keeps the control plane centralized in SQL while giving each onboarded
tenant a clean runtime-doc boundary for publishing, content, and staged
document workloads.

## Required Boundaries

- Tenant ID must be resolved before domain operations
- Feature entitlements must be evaluated per tenant and plan
- Audit, AI usage, and import jobs must always include tenant context

## India-First Defaults

- INR pricing and tax assumptions in Wave 1
- IST-aware scheduling and booking defaults
- Domestic travel and hotel workflows prioritized in templates
- Compliance extension points left open for later sector-specific work
