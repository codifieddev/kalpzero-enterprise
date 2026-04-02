# 01 Repo Architecture

## Monorepo Layout

- `apps/web`: operator console and public publishing shell
- `apps/api`: canonical FastAPI service
- `apps/worker`: background jobs and import runners
- `packages/contracts`: TypeScript domain contracts
- `packages/ui`: shared shell components and visual primitives
- `packages/config`: shared config templates
- `adapters/*`: migration and source mapping definitions
- `docs/*`: architecture and execution decisions

## Runtime Topology

```mermaid
flowchart LR
    "Web (Next.js)" --> "API (FastAPI)"
    "Worker" --> "API (FastAPI)"
    "API (FastAPI)" --> "Primary SQL"
    "API (FastAPI)" --> "Mongo / document store"
    "API (FastAPI)" --> "Redis / queue"
    "Worker" --> "Redis / queue"
    "Legacy and external sources" --> "Import pipeline"
    "Import pipeline" --> "Canonical data model"
```

## Experience Topology

```mermaid
flowchart LR
    "Business Blueprint" --> "Public Next.js runtime"
    "Business Blueprint" --> "Admin shell runtime"
    "Business Blueprint" --> "Future mobile runtime"
    "Runtime documents" --> "Public Next.js runtime"
    "Runtime documents" --> "Discovery materialization"
    "Common API" --> "Business Blueprint"
    "Common API" --> "Runtime documents"
    "Common API" --> "Vertical packs"
```

## Design Rules

- Backend authority lives in FastAPI, not in frontend route handlers
- Shared contracts come before app-specific DTO duplication
- Background work is explicit, not hidden inside request-response handlers
- Legacy extraction is isolated behind adapters and mapping manifests
- Tenant design flexibility is expressed through blueprints, themes, and block
  schemas, not arbitrary frontend forks or raw script injection

## Storage Decision

- Control plane and transactional runtime stay in SQL
- Flexible runtime documents and AI knowledge live in MongoDB
- Queue, cache, and rate limiting live in Redis
- The old "3-set" idea is preserved as three logical data layers, not three
  Mongo databases
