# KalpZero Enterprise Canonical Rebuild Plan

## Summary
Create a new sibling repo at `/Users/apple/Desktop/WORK/GIT/kalpzero-enterprise` and treat the current repo at `/Users/apple/Desktop/WORK/GIT/kalpzero` as `legacy-reference` only. The new repo is the sole canonical product and is built as a split monorepo: `web` (Next.js), `api` (FastAPI), `worker`, shared contracts, shared UI, and decision-grade docs.

Wave 1 is `eCommerce + Travel + Hotel`, with `India-first`, `hybrid multi-tenant`, and `AI foundation in Wave 1`. External project databases feed the new platform through one-way canonical sync adapters; the new platform becomes the source of truth.

## Implementation Changes
### Repo and platform structure
- Create a new monorepo with:
  - `apps/web`: Next.js operator app + public publishing
  - `apps/api`: FastAPI canonical backend
  - `apps/worker`: background jobs for import, indexing, publishing, notifications, AI ingestion
  - `packages/contracts`: DTOs, API schemas, event schemas, registry schemas
  - `packages/ui`: shared design system and admin/public shells
  - `packages/config`: environment, lint, TS, Python, CI templates
  - `docs/`: architecture, roadmap, migration, vertical specs, runbooks
  - `adapters/legacy-kalpzero`: extraction and mapping specs from the current repo
  - `adapters/external-sources`: mapping specs for the user’s separate project databases
- Keep current repo read-only for reference extraction of:
  - business catalogs and vocabulary logic
  - travel package contracts and itinerary concepts
  - customer lifecycle patterns
  - builder/public publishing concepts
  - discovery/SEO surface ideas

### Core architecture
- Use FastAPI as the canonical backend, not Next route handlers.
- Make all authorization fail closed. No fallback allow behavior.
- Replace current JWT/secret fallback behavior with mandatory env validation at boot; app must not start with default secrets.
- Standardize tenancy around:
  - shared control plane
  - tenant-scoped runtime
  - optional dedicated DB/storage/AI profile per enterprise tenant
- Add first-class enterprise subsystems from the start:
  - audit log
  - job queue
  - event bus/outbox
  - import pipeline
  - observability and usage metering
  - feature entitlement engine
  - backup/export framework
  - SSO-ready auth boundary
- AI in Wave 1 includes:
  - provider config and governance
  - tenant-scoped model/runtime settings
  - knowledge ingestion pipeline
  - usage tracking and auditability
  - prompt/policy boundaries
- Defer advanced agentic automations to later waves.

### Canonical domain model
- Shared core entities:
  - `Agency`, `Tenant`, `User`, `Membership`, `Role`, `Permission`, `FeatureFlag`
  - `BrandProfile`, `DomainProfile`, `Page`, `MediaAsset`, `Form`, `FormResponse`
  - `Customer`, `Booking`, `Invoice`, `PaymentRecord`, `ImportJob`, `AuditEvent`, `AiSession`
- Vertical packs:
  - `commerce`: product, category, variant, cart, order, coupon, shipment, tax, payment
  - `travel`: package, itinerary day, departure, hotel ref, activity ref, transfer ref, traveler, lead
  - `hotel`: property, room type, room, inventory calendar, reservation, check-in/out, housekeeping, maintenance, meal plan, staff
  - later `real_estate`, `clinic`, `single_doctor`, `school`, `lms`
- Do not reuse generic `products` as the runtime model for every vertical.
- Eliminate duplicate hotel schemas; define one canonical hotel model only.

### Migration and reuse strategy
- Build one-way canonical import adapters from:
  - current KalpZero Mongo data
  - the user’s separate vertical project databases
- Import pipeline stages:
  - source extraction
  - normalization
  - entity mapping
  - dedupe and identity resolution
  - validation
  - canonical write
  - audit trail and import report
- Reuse from current repo only when behavior is already sound:
  - travel package structure and public package concepts
  - customer linkage ideas
  - attribute/business catalog concepts
  - selected builder/public rendering ideas
- Do not port directly:
  - root auth/session code
  - current permission engine
  - forced module rules
  - duplicate hotel/travel runtime routes
  - fallback sample production behavior
  - onboarding demo seeding into real tenant runtime

## Public APIs, Interfaces, and Types
- Canonical API families:
  - `/auth/*`: login, session, SSO handshake, tenant switch, role context
  - `/platform/*`: agencies, tenants, plans, infra profiles, registry snapshot
  - `/imports/*`: source registration, import jobs, mapping configs, reports
  - `/commerce/*`, `/travel/*`, `/hotel/*`: vertical APIs by canonical pack
  - `/publishing/*`: domains, SEO, public routes, preview/live publishing
  - `/ai/*`: runtime config, sessions, knowledge ingestion, usage
- Shared contract package must define:
  - tenant and agency DTOs
  - registry/module/feature DTOs
  - vertical DTOs per pack
  - import job/result DTOs
  - audit event DTOs
  - AI runtime/session DTOs
- Event schemas must be explicit for:
  - tenant provisioned
  - import completed/failed
  - order created
  - booking created/updated
  - invoice issued
  - content published
  - AI usage recorded

## Documentation Pack and Roadmap
- Create these docs first in the new repo:
  - `00_CANONICAL_PRODUCT_BRIEF.md`
  - `01_REPO_ARCHITECTURE.md`
  - `02_TENANCY_AND_INFRA_MODEL.md`
  - `03_AUTH_RBAC_AUDIT_MODEL.md`
  - `04_CANONICAL_DATA_MODEL.md`
  - `05_IMPORT_AND_SYNC_ARCHITECTURE.md`
  - `06_WAVE1_COMMERCE_SPEC.md`
  - `07_WAVE1_TRAVEL_SPEC.md`
  - `08_WAVE1_HOTEL_SPEC.md`
  - `09_AI_FOUNDATION_SPEC.md`
  - `10_PUBLIC_PUBLISHING_AND_DISCOVERY.md`
  - `11_TEST_STRATEGY_AND_QUALITY_GATES.md`
  - `12_EXECUTION_ROADMAP_90_DAYS.md`
- 90-day roadmap:
  - Phase 0: repo bootstrap, CI, env validation, contracts skeleton, docs skeleton
  - Phase 1: auth, tenancy, registry, audit, job framework, import framework
  - Phase 2: commerce pack and publishing foundation
  - Phase 3: travel pack and travel public pages
  - Phase 4: hotel pack with unified PMS model
  - Phase 5: external source adapters and staged migration
  - Phase 6: next vertical specs for real estate, clinic, doctor site, school, LMS

## Test Plan
- Architecture gates:
  - backend must fail startup on missing secrets or invalid infra config
  - permission checks must deny on missing permission definitions
  - tenant isolation tests for shared and dedicated infra modes
- Migration tests:
  - import dry-run with validation-only mode
  - duplicate detection and idempotent re-import
  - mapping correctness from legacy KalpZero travel/hotel/commerce data
- Domain tests:
  - commerce order lifecycle
  - travel package creation and public rendering
  - hotel reservation to check-in/out lifecycle with room status integrity
- Platform tests:
  - registry snapshot by tenant plan and feature entitlement
  - audit event creation for privileged operations
  - AI runtime config scoping and usage metering
- Acceptance scenarios:
  - onboard tenant, import source data, publish public site, transact in Wave 1 domains, inspect audit/import history

## Assumptions and Defaults
- New sibling repo name: `kalpzero-enterprise`.
- Current repo remains as reference only; no new feature work should continue there except extraction support.
- Primary market is India-first, with extension points for later global compliance.
- Deployment model is hybrid multi-tenant with optional dedicated enterprise infra.
- FastAPI is the canonical backend; Next.js is the canonical operator/public frontend.
- External source systems are integrated through one-way canonical sync, not dual-write.
- Wave 1 implementation targets only Commerce, Travel, and Hotel.
- Real Estate, Doctor Clinic, Single Doctor Website, School Management, and LMS are planned as later vertical packs on the same core platform.
