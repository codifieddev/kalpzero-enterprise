export type AiProvider = "openai" | "azure-openai" | "anthropic" | "vertex";

export interface AiRuntimePolicyDto {
  tenantId: string;
  provider: AiProvider;
  model: string;
  maxInputTokens: number;
  maxOutputTokens: number;
  piiRedactionEnabled: boolean;
  requiresHumanApproval: boolean;
}

export interface AiSessionDto {
  id: string;
  tenantId: string;
  actorUserId: string;
  purpose: "assistant" | "workflow" | "knowledge_ingestion";
  createdAt: string;
}

export interface AiUsageRecordDto {
  id: string;
  tenantId: string;
  provider: AiProvider;
  model: string;
  inputTokens: number;
  outputTokens: number;
  costMinor: number;
  currency: string;
  recordedAt: string;
}
