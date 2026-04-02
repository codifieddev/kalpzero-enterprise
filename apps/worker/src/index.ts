import type { DomainEventDto, ImportJobDto } from "@kalpzero/contracts";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

const queues = {
  imports: "kz.imports",
  publishing: "kz.publishing",
  notifications: "kz.notifications",
  aiIngestion: "kz.ai.ingestion",
  auditOutbox: "kz.audit.outbox"
} as const;

type AdapterManifest = {
  adapter_id?: string;
  mode?: string;
  source_root?: string;
  source_type?: string;
  vertical_pack?: string;
  collections?: Array<{ name?: string; canonical_target?: string; action?: string }>;
  entities?: Array<{ source_entity?: string; canonical_entity?: string }>;
};

const workerConsumers = [
  {
    eventName: "tenant.provisioned",
    queue: queues.imports,
    handler: "provision-tenant-runtime"
  },
  {
    eventName: "import.job.queued",
    queue: queues.imports,
    handler: "run-canonical-import"
  },
  {
    eventName: "hotel.reservation.updated",
    queue: queues.notifications,
    handler: "sync-hotel-ops-ledger"
  },
  {
    eventName: "commerce.order.created",
    queue: queues.notifications,
    handler: "dispatch-commerce-order-workflows"
  },
  {
    eventName: "travel.lead.updated",
    queue: queues.notifications,
    handler: "sync-travel-lead-pipeline"
  },
  {
    eventName: "publishing.content.published",
    queue: queues.publishing,
    handler: "refresh-public-surface"
  },
  {
    eventName: "ai.usage.recorded",
    queue: queues.auditOutbox,
    handler: "persist-usage-ledger"
  }
] as const;

const starterImportJob: ImportJobDto = {
  id: "job-demo-001",
  tenantId: "tenant_demo",
  sourceId: "legacy-kalpzero",
  mode: "dry_run",
  status: "queued",
  requestedAt: "2026-03-31T00:00:00Z"
};

const starterEvent: DomainEventDto = {
  id: "evt-demo-001",
  name: "tenant.provisioned",
  tenantId: "tenant_demo",
  aggregateId: "tenant_demo",
  occurredAt: "2026-03-31T00:00:00Z",
  payload: {
    infraMode: "shared",
    verticalPacks: ["commerce", "travel", "hotel"]
  }
};

function repoRoot(): string {
  const currentDir = dirname(fileURLToPath(import.meta.url));
  return resolve(currentDir, "../../..");
}

function collectYamlFiles(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      return collectYamlFiles(fullPath);
    }

    return entry.name.endsWith(".yaml") ? [fullPath] : [];
  });
}

function loadAdapterSummaries() {
  const adaptersRoot = join(repoRoot(), "adapters");
  const yamlFiles = collectYamlFiles(adaptersRoot);

  return yamlFiles.map((filePath) => {
    const raw = readFileSync(filePath, "utf8");
    const manifest = YAML.parse(raw) as AdapterManifest;
    return {
      adapterId: manifest.adapter_id ?? "unknown",
      sourceType: manifest.source_type ?? manifest.source_root ?? "legacy-reference",
      mode: manifest.mode ?? "unspecified",
      targets:
        manifest.collections?.map((collection) => collection.canonical_target ?? collection.name ?? "unknown") ??
        manifest.entities?.map((entity) => entity.canonical_entity ?? entity.source_entity ?? "unknown") ??
        []
    };
  });
}

function logBootstrapState() {
  const adapters = loadAdapterSummaries();
  console.log("KalpZero Enterprise worker bootstrap");
  console.table(queues);
  console.table(workerConsumers);
  console.table(adapters);
  console.log("Seed import job:", starterImportJob);
  console.log("Seed event:", starterEvent);
}

logBootstrapState();
