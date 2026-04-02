# Environment Rules

- All secrets are mandatory in non-test environments.
- No default JWT, encryption, or provider keys are permitted.
- `apps/api` owns boot-time env validation and must fail startup on missing or
  weak values.
- Tenant-specific secrets should be stored in a secrets manager, not in source
  control or tenant records.
- Use `KALPZERO_CONTROL_DATABASE_URL` for the SQL control plane.
- Use `KALPZERO_RUNTIME_MONGO_URL` and `KALPZERO_RUNTIME_MONGO_DB` for the
  runtime document store.
- Use `KALPZERO_RUNTIME_DOC_STORE_MODE` to switch the runtime document layer
  between `mongo` and `memory`. `memory` is reserved for tests and local
  scaffolding.
- Use `KALPZERO_OPS_REDIS_URL` for queue, cache, and rate-limit infrastructure.
