# Legacy KalpZero Adapter

This adapter treats `/Users/apple/Desktop/WORK/GIT/kalpzero` as
`legacy-reference`. The purpose is extraction and mapping, not direct runtime
reuse.

## Reuse Targets

- Business template and catalog ideas from
  `/Users/apple/Desktop/WORK/GIT/kalpzero/platform/registry/modules`
- Travel package and itinerary concepts from
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/travel`
- Customer and booking linkage patterns from
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/customers` and
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/bookings`
- Public discovery and SEO surface concepts from
  `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/(public)/discover`

## Explicit Non-Port List

- `/Users/apple/Desktop/WORK/GIT/kalpzero/engine/permission-engine/index.ts`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/jwt.ts`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/secret-crypto.ts`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/lib/module-rules.ts`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/hotel`
- `/Users/apple/Desktop/WORK/GIT/kalpzero/src/app/api/travel/hotel`

## Migration Rule

Every extraction must map into canonical contracts in `packages/contracts` and
must record source system, source key, import job, and validation outcome.
