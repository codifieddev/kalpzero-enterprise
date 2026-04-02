# 05 Import And Sync Architecture

## Pipeline Stages

- Source registration
- Extraction
- Normalization
- Source-to-canonical mapping
- Identity resolution and dedupe
- Validation
- Canonical write
- Audit and import reporting

## Import Modes

- `dry_run`: validate and report without writing
- `execute`: write canonical entities and emit events

## Core Guarantees

- Idempotent re-runs
- Source lineage on every imported entity
- Explicit reject and warning buckets
- Human-readable import report per job

## Flow

```mermaid
flowchart TD
    "Source system" --> "Extractor"
    "Extractor" --> "Normalizer"
    "Normalizer" --> "Mapper"
    "Mapper" --> "Deduper"
    "Deduper" --> "Validator"
    "Validator" --> "Dry run report"
    "Validator" --> "Canonical writer"
    "Canonical writer" --> "Audit log"
    "Canonical writer" --> "Outbox events"
```
