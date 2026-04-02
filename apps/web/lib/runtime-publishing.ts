import type {
  BusinessBlueprintDto,
  PublicSitePayloadDto,
  ThemeTokensDto
} from "@kalpzero/contracts";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  process.env.KALPZERO_PUBLIC_API_URL ??
  "http://localhost:8000";

function titleCaseFromSlug(value: string) {
  return value
    .split(/[-_/]/g)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function fallbackTheme(tenantSlug: string, mode: "public" | "admin"): ThemeTokensDto {
  const brandName = titleCaseFromSlug(tenantSlug);
  if (mode === "admin") {
    return {
      brandName: `${brandName} Admin`,
      primaryColor: "#142235",
      accentColor: "#d65d0e",
      surfaceColor: "#f4f7fb",
      inkColor: "#142235",
      mutedColor: "#697687",
      headingFont: "Space Grotesk",
      bodyFont: "Space Grotesk",
      radiusScale: "soft",
      density: "compact",
      motionProfile: "minimal"
    };
  }

  return {
    brandName,
    primaryColor: "#1d4f91",
    accentColor: "#d65d0e",
    surfaceColor: "#f9f6f1",
    inkColor: "#142235",
    mutedColor: "#697687",
    headingFont: "Fraunces",
    bodyFont: "Space Grotesk",
    radiusScale: "rounded",
    density: "comfortable",
    motionProfile: "calm"
  };
}

function fallbackBlueprintPreview(tenantSlug: string): BusinessBlueprintDto {
  const brandName = titleCaseFromSlug(tenantSlug);
  return {
    tenantId: tenantSlug,
    tenantSlug,
    version: 1,
    businessLabel: brandName,
    verticalPacks: ["commerce", "hotel"],
    enabledModules: ["publishing.pages", "publishing.discovery", "commerce", "hotel"],
    publicTheme: fallbackTheme(tenantSlug, "public"),
    adminTheme: fallbackTheme(tenantSlug, "admin"),
    publicNavigation: [
      { label: "Home", href: "/", kind: "link", icon: "home" },
      { label: "Catalog", href: "/catalog", kind: "link", icon: "bag" },
      { label: "Stay", href: "/stay", kind: "link", icon: "key" },
      { label: "Contact", href: "/contact", kind: "cta", icon: "mail" }
    ],
    adminNavigation: [
      { label: "Overview", href: "/admin", kind: "module", icon: "dashboard" },
      { label: "Publishing", href: "/admin/publishing", kind: "module", icon: "paintbrush" },
      { label: "Operations", href: "/admin/hotel", kind: "module", icon: "stack" }
    ],
    routes: [
      { key: "home", path: "/", pageSlug: "home", visibility: "public" },
      { key: "catalog", path: "/catalog", pageSlug: "catalog", visibility: "public" },
      { key: "stay", path: "/stay", pageSlug: "stay", visibility: "public" }
    ],
    dashboardWidgets: [
      {
        key: "orders",
        title: "Orders",
        metric: "24",
        description: "Observe catalog-driven transactions."
      },
      {
        key: "occupancy",
        title: "Occupancy",
        metric: "81%",
        description: "Preview hospitality operations from the same blueprint."
      }
    ],
    vocabulary: {
      customer: "Guest",
      order: "Order",
      booking: "Reservation",
      location: "Property"
    },
    mobileCapabilities: ["push_notifications", "digital_checkin"]
  };
}

function fallbackPublicSitePayload(tenantSlug: string, pageSlug: string): PublicSitePayloadDto {
  const blueprint = fallbackBlueprintPreview(tenantSlug);
  const pageTitle = pageSlug === "home" ? blueprint.businessLabel : `${blueprint.businessLabel} ${titleCaseFromSlug(pageSlug)}`;

  return {
    tenantSlug,
    businessLabel: blueprint.businessLabel,
    publicTheme: blueprint.publicTheme,
    publicNavigation: blueprint.publicNavigation,
    vocabulary: blueprint.vocabulary,
    page: {
      id: `${tenantSlug}:${pageSlug}`,
      tenantSlug,
      pageSlug,
      routePath: pageSlug === "home" ? "/" : `/${pageSlug}`,
      title: pageTitle,
      status: "live",
      seoTitle: pageTitle,
      seoDescription: "Blueprint-driven public page served from the common Kalp runtime.",
      layout: pageSlug === "catalog" ? "catalog" : "landing",
      blocks: [
        {
          id: "hero",
          kind: "hero",
          eyebrow: blueprint.businessLabel,
          headline: `A tenant-specific ${titleCaseFromSlug(pageSlug)} page without a tenant-specific codebase.`,
          body: "Theme tokens, routes, and content blocks come from one blueprint contract that can later power web, admin, and native surfaces.",
          ctaLabel: "Open Admin Preview",
          ctaHref: `/studio/${tenantSlug}`,
          items: []
        },
        {
          id: "features",
          kind: "feature_grid",
          headline: "Why this architecture scales",
          body: "Each business gets SEO and design flexibility without forking the platform.",
          items: [
            {
              title: "Next.js public runtime",
              description: "SSR and SEO-friendly pages rendered from runtime docs."
            },
            {
              title: "Common API",
              description: "Business logic, modules, and data stay centralized."
            },
            {
              title: "Theme and block registry",
              description: "Distinct UI direction with reusable components."
            }
          ]
        },
        {
          id: "stats",
          kind: "stat_strip",
          headline: "Blueprint Stats",
          items: [
            { title: "Routes", value: `${blueprint.routes.length}` },
            { title: "Modules", value: `${blueprint.enabledModules.length}` },
            { title: "Widgets", value: `${blueprint.dashboardWidgets.length}` }
          ]
        }
      ]
    },
    discovery: {
      tenantSlug,
      headline: `${blueprint.businessLabel} discovery surface`,
      summary: "Discovery cards can be materialized from runtime documents for SEO and search exposure.",
      tags: blueprint.verticalPacks,
      cards: blueprint.routes.map((route) => ({
        title: titleCaseFromSlug(route.key),
        summary: `Public route ${route.path} driven by the blueprint registry.`,
        href: route.path,
        tags: blueprint.verticalPacks
      }))
    }
  };
}

async function fetchJson<T>(url: string): Promise<T | null> {
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export async function getPublicSitePayload(
  tenantSlug: string,
  pageSlug: string
): Promise<PublicSitePayloadDto> {
  const payload = await fetchJson<PublicSitePayloadDto>(
    `${apiBaseUrl}/publishing/public/${tenantSlug}/site?page_slug=${encodeURIComponent(pageSlug)}`
  );
  return payload ?? fallbackPublicSitePayload(tenantSlug, pageSlug);
}

export async function getBlueprintPreview(tenantSlug: string): Promise<BusinessBlueprintDto> {
  const payload = await fetchJson<BusinessBlueprintDto>(
    `${apiBaseUrl}/publishing/public/${tenantSlug}/blueprint-preview`
  );
  return payload ?? fallbackBlueprintPreview(tenantSlug);
}
