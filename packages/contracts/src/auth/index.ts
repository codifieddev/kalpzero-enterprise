export type AuthProvider = "password" | "google" | "microsoft" | "saml" | "otp";

export interface UserDto {
  id: string;
  email: string;
  fullName: string;
  status: "active" | "invited" | "disabled";
  createdAt: string;
}

export interface MembershipDto {
  id: string;
  userId: string;
  tenantId: string;
  roleIds: string[];
  isPrimary: boolean;
}

export interface SessionContextDto {
  userId: string;
  tenantId: string;
  roleKeys: string[];
  featureFlags: string[];
  authProvider: AuthProvider;
}

export interface LoginRequestDto {
  email: string;
  password: string;
  tenantSlug?: string;
}

export interface LoginResponseDto {
  accessToken: string;
  expiresAt: string;
  session: SessionContextDto;
}
