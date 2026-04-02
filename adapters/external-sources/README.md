# External Source Adapters

This folder defines the canonical import contract for the user's separate
vertical projects and their extended databases.

## Adapter Contract

- Register source identity and owner
- Capture connection profile and secrets reference
- Describe extraction query or collection scope
- Define source-to-canonical field mappings
- Define dedupe keys and conflict resolution strategy
- Define dry-run validation rules
- Emit import report and audit event

The platform source of truth remains KalpZero Enterprise after import.
