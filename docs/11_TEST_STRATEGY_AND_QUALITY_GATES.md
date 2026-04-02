# 11 Test Strategy And Quality Gates

## Architecture Gates

- API boot fails on missing or weak secrets
- Permission checks deny if definitions are absent
- Tenant boundary tests cover shared and dedicated infra paths
- Tenant provisioning denies unsupported or infra-invalid onboarding requests

## Migration Gates

- Dry-run imports produce reports without writes
- Re-runs are idempotent
- Duplicate detection is deterministic
- Legacy KalpZero travel, hotel, and commerce mappings are verified

## Domain Gates

- Commerce order lifecycle
- Travel package and departure lifecycle
- Hotel reservation and room state integrity

## Platform Gates

- Registry snapshot respects plan and feature entitlements
- Audit events exist for privileged operations
- AI usage is scoped per tenant and recorded
- Onboarding readiness report reflects approved Wave 1 verticals and infra
  posture before tenant creation
