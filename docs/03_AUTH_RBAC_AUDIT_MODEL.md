# 03 Auth RBAC Audit Model

## Why Rebuild

The legacy repo contains unsafe patterns that cannot be the base for enterprise
delivery:

- `/Users/apple/Desktop/WORK/GIT/kalpzero/engine/permission-engine/index.ts` can allow access when permission specs are missing
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/jwt.ts` falls back to a default secret
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/secret-crypto.ts` falls back to a predictable secret
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/module-rules.ts` can force-enable modules regardless of contract

## Canonical Rules

- Missing permission definition means deny
- Missing or weak secrets means boot failure
- Role grants are explicit and versioned
- Privileged operations emit audit events
- SSO support is built as a boundary, even if password auth is the first mode

## Audit Events

Audit events must capture:

- Actor
- Tenant
- Subject type and subject ID
- Action
- Metadata
- Timestamp
- Correlated request or import job ID
