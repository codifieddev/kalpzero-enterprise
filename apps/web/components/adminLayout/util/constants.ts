import type { NavEntrySpec } from "@core/contracts/registry";

export const SECTION_META: Record<
  string,
  { label: string; labelKey: string; headingClass: string; dotClass: string }
> = {
  commerce: {
    label: "Commerce",
    labelKey: "section.commerce",
    headingClass: "text-purple-500/70",
    dotClass: "bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.8)]",
  },
  operations: {
    label: "Operations",
    labelKey: "section.operations",
    headingClass: "text-orange-500/70",
    dotClass: "bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.8)]",
  },
  content: {
    label: "Content",
    labelKey: "section.content",
    headingClass: "text-emerald-500/70",
    dotClass: "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]",
  },
  engagement: {
    label: "Engagement",
    labelKey: "section.engagement",
    headingClass: "text-amber-500/70",
    dotClass: "bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]",
  },
  modules: {
    label: "Apps",
    labelKey: "section.modules",
    headingClass: "text-indigo-500/70",
    dotClass: "bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.7)]",
  },
};

export const SECTION_ORDER: Record<string, number> = {
  commerce: 10,
  operations: 20,
  content: 30,
  engagement: 40,
  modules: 50,
};

export const FALLBACK_MODULE_NAVS: Record<string, NavEntrySpec[]> = {
  website: [
    {
      id: "nav.website.pages",
      label: "Website Pages",
      path: "/pages",
      parentId: "group.content",
      requiredPermissionId: "perm.website.read",
    },
    {
      id: "nav.website.forms",
      label: "Forms",
      path: "/forms",
      parentId: "group.content",
      requiredPermissionId: "perm.website.forms.read",
    },
  ],
  branding: [
    {
      id: "nav.branding",
      label: "Brand Kit",
      path: "/branding",
      parentId: "group.engagement",
      requiredPermissionId: "perm.branding.read",
    },
  ],
  products: [
    {
      id: "nav.products",
      label: "Products",
      path: "/ecommerce",
      parentId: "group.commerce",
      requiredPermissionId: "perm.products.read",
    },
    {
      id: "nav.products.categories",
      label: "Categories",
      path: "/ecommerce/categories",
      parentId: "group.commerce",
      requiredPermissionId: "perm.products.read",
    },
    {
      id: "nav.products.attributes",
      label: "Attribute Sets",
      path: "/ecommerce/attributes",
      parentId: "group.commerce",
      requiredPermissionId: "perm.products.read",
    },
    {
      id: "nav.travel.packages",
      label: "Travel Packages",
      path: "/travel/packages",
      parentId: "group.commerce",
      requiredPermissionId: "perm.products.read",
    },
  ],
  ecommerce: [
    {
      id: "nav.ecommerce.orders",
      label: "Orders",
      path: "/ecommerce/orders",
      parentId: "group.operations",
      requiredPermissionId: "perm.ecommerce.read",
    },
    {
      id: "nav.ecommerce.payments-shipping",
      label: "Payments & Shipping",
      path: "/commerce/payments-shipping",
      parentId: "group.operations",
      requiredPermissionId: "perm.ecommerce.read",
    },
  ],
  bookings: [
    {
      id: "nav.bookings",
      label: "Bookings",
      path: "/bookings",
      parentId: "group.engagement",
      requiredPermissionId: "perm.bookings.read",
    },
  ],
  marketing: [
    {
      id: "nav.marketing",
      label: "Marketing",
      path: "/marketing",
      parentId: "group.engagement",
      requiredPermissionId: "perm.marketing.read",
    },
  ],
  blog: [
    {
      id: "nav.blog",
      label: "Blog",
      path: "/blog",
      parentId: "group.content",
      requiredPermissionId: "perm.blog.read",
    },
  ],
  portfolio: [
    {
      id: "nav.portfolio",
      label: "Portfolio",
      path: "/portfolio",
      parentId: "group.content",
      requiredPermissionId: "perm.portfolio.read",
    },
  ],
  media: [
    {
      id: "nav.media",
      label: "Media Library",
      path: "/media",
      parentId: "group.content",
      requiredPermissionId: "perm.media.read",
    },
  ],
  invoicing: [
    {
      id: "nav.invoicing",
      label: "Invoicing",
      path: "/invoices",
      parentId: "group.operations",
      requiredPermissionId: "perm.invoicing.read",
    },
  ],
  hotel_management: [
    {
      id: "nav.hotelManagement",
      label: "Hotel Management",
      path: "/hotel-management",
      parentId: "group.operations",
      requiredPermissionId: "perm.hotel_management.read",
    },
  ],
  tour_management: [
    {
      id: "nav.tourManagement",
      label: "Tour Management",
      path: "/tour-management",
      parentId: "group.operations",
      requiredPermissionId: "perm.tour_management.read",
    },
  ],
  real_estate: [
    {
      id: "nav.real_estate",
      label: "Real Estate",
      path: "/real-estate",
      parentId: "group.commerce",
      requiredPermissionId: "perm.real_estate.read",
    },
  ],
  source: [
    {
      id: "nav.source",
      label: "Source",
      path: "/sources",
      parentId: "group.modules",
      requiredPermissionId: "perm.source.read",
    },
  ],
  kalpbodh: [
    {
      id: "nav.kalpbodh",
      label: "KalpBodh",
      path: "/kalpbodh",
      parentId: "group.engagement",
      requiredPermissionId: "perm.kalpbodh.read",
    },
  ],
};
