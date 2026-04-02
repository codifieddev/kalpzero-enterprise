export type InfraMode = "shared" | "dedicated";
export type VerticalPack =
  | "commerce"
  | "travel"
  | "hotel"
  | "real_estate"
  | "clinic"
  | "single_doctor"
  | "school"
  | "lms";

export interface AgencyDto {
  id: string;
  slug: string;
  name: string;
  region: "in" | "global";
  ownerUserId: string;
  createdAt: string;
}

export interface TenantDto {
  id: string;
  agencyId: string;
  slug: string;
  displayName: string;
  infraMode: InfraMode;
  verticalPacks: VerticalPack[];
  featureFlags: string[];
  dedicatedProfileId?: string;
  createdAt: string;
}

export interface RoleDto {
  id: string;
  tenantId: string;
  key: string;
  name: string;
  permissions: string[];
}

export interface PermissionDefinitionDto {
  key: string;
  module: string;
  description: string;
  riskLevel: "low" | "medium" | "high" | "critical";
}

export interface FeatureFlagDto {
  key: string;
  description: string;
  enabledByDefault: boolean;
  verticalPack?: VerticalPack;
}

export interface RegistrySnapshotDto {
  tenantId: string;
  modules: string[];
  features: string[];
  generatedAt: string;
}
