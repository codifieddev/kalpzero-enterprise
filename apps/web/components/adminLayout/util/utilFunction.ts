import React from "react";
import { Layers } from "lucide-react";
import { resolveAdminIcon } from "@/lib/admin-icon-catalog";
import type { NavEntrySpec } from "@core/contracts/registry";

/**
 * Resolves an icon component for a navigation entry.
 * Defaults to the 'Layers' icon if none is found.
 */
export function resolveNavIcon(icon?: string): React.ElementType {
  const resolved = resolveAdminIcon(icon);
  if (resolved) return resolved;
  return Layers;
}

/**
 * Checks if a given path is active based on the current pathname.
 */
export function isPathActive(pathname: string, href: string): boolean {
  if (pathname === href) return true;
  if (href === "/") return pathname === "/";
  return pathname.startsWith(`${href}/`);
}

/**
 * Attempts to infer a module key (e.g., "products", "website") from a navigation specification.
 */
export function inferModuleKeyFromNav(nav: NavEntrySpec): string | null {
  if (typeof nav?.requiredPermissionId === "string") {
    const match = nav.requiredPermissionId.match(/^perm\.([^.]+)\./);
    if (match?.[1]) return match[1];
  }

  if (typeof nav?.id === "string" && nav.id.startsWith("nav.")) {
    const inferred = nav.id.slice(4).split(".")[0]?.trim();
    if (inferred) return inferred;
  }

  if (typeof nav?.path === "string") {
    const firstSegment = nav.path.replace(/^\//, "").split("/")[0]?.trim();
    if (firstSegment) return firstSegment;
  }

  return null;
}

/**
 * Normalizes a parent section ID for sidebar grouping.
 */
export function normalizeSectionId(parentId: unknown): string {
  if (typeof parentId !== "string") return "modules";
  const trimmed = parentId.trim().toLowerCase();
  if (!trimmed) return "modules";
  if (trimmed.startsWith("group.")) return trimmed.replace("group.", "");
  if (trimmed.startsWith("section.")) return trimmed.replace("section.", "");
  return trimmed;
}

/**
 * Applies navigation overrides (label, path, icon, etc.) from a registry snapshot.
 */
export function applyNavOverride(
  nav: NavEntrySpec,
  overrides: Record<string, Partial<NavEntrySpec>>,
): NavEntrySpec {
  const override = overrides[nav.id];
  if (!override) return nav;

  return {
    ...nav,
    label:
      typeof override.label === "string" && override.label.trim()
        ? override.label
        : nav.label,
    path:
      typeof override.path === "string" && override.path.trim()
        ? override.path
        : nav.path,
    icon:
      typeof override.icon === "string" && override.icon.trim()
        ? override.icon
        : nav.icon,
    parentId:
      typeof override.parentId === "string" && override.parentId.trim()
        ? override.parentId
        : nav.parentId,
  };
}

/**
 * Normalizes business context strings for consistent lookup.
 */
export function normalizeBusinessContext(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/**
 * Checks if a string contains signals related to travel or hospitality business.
 */
export function hasTravelSignals(value: string): boolean {
  const normalized = normalizeBusinessContext(value);
  if (!normalized) return false;
  const travelTokens = [
    "travel",
    "tour",
    "itinerary",
    "trip",
    "vacation",
    "hospitality",
  ];
  return travelTokens.some((token) => normalized.includes(token));
}
