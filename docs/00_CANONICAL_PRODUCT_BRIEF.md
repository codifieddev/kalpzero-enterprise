# 00 Canonical Product Brief

## Objective

KalpZero Enterprise is the canonical rebuild of KalpZero as a vertical
operations platform for businesses. It replaces the current pattern of one
monolithic app trying to impersonate every business type through loose modules.

## Product Outcome

- One core platform for tenancy, auth, registry, audit, imports, publishing, and AI
- Vertical packs for business-specific workflows and data models
- Business blueprints that let each tenant change vocabulary, routes, themes,
  widgets, and public/admin experience without forking the codebase
- Enterprise-grade rollout for India-first businesses with optional dedicated infra
- Clean migration path from existing KalpZero data and the user's separate project databases

## Wave 1 Scope

- Commerce
- Travel
- Hotel

## Later Packs

- Real estate
- Doctor clinic
- Single doctor website
- School management
- LMS

## Success Criteria

- New tenants can be onboarded without demo data pollution
- All privilege checks deny when definitions are missing
- Hotel exists as one unified PMS model
- Imports are dry-runnable, idempotent, and auditable
- AI is governed per tenant with usage tracking and approval boundaries
