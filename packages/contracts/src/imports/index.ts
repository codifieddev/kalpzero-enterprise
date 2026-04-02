export type ImportSourceType = "legacy-kalpzero" | "postgres" | "mysql" | "mongodb" | "api";

export interface ImportSourceDto {
  id: string;
  tenantId: string;
  name: string;
  sourceType: ImportSourceType;
  connectionProfileKey: string;
}

export interface ImportJobDto {
  id: string;
  tenantId: string;
  sourceId: string;
  mode: "dry_run" | "execute";
  status: "queued" | "running" | "succeeded" | "failed";
  requestedAt: string;
  finishedAt?: string;
}

export interface ImportReportDto {
  jobId: string;
  entitiesRead: number;
  entitiesValidated: number;
  entitiesWritten: number;
  duplicatesDetected: number;
  warnings: string[];
  errors: string[];
}
