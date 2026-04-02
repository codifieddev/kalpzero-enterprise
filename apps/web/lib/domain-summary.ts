import type { VerticalPack } from "@kalpzero/contracts";

export interface VerticalSummary {
  pack: VerticalPack;
  status: "wave-1" | "planned";
  title: string;
  description: string;
}

export const verticalSummaries: VerticalSummary[] = [
  {
    pack: "commerce",
    status: "wave-1",
    title: "Commerce operating core",
    description: "Catalog, pricing, orders, payments, fulfillment, and publishing."
  },
  {
    pack: "travel",
    status: "wave-1",
    title: "Travel orchestration",
    description: "Packages, departures, itineraries, leads, and public trip commerce."
  },
  {
    pack: "hotel",
    status: "wave-1",
    title: "Unified hotel PMS",
    description: "Property, room inventory, reservations, housekeeping, and billing."
  },
  {
    pack: "real_estate",
    status: "planned",
    title: "Real estate sales ops",
    description: "Inventory, projects, site visits, brokers, leads, and deal progression."
  },
  {
    pack: "clinic",
    status: "planned",
    title: "Clinic operations",
    description: "Appointments, patient records, prescriptions, billing, and follow-ups."
  },
  {
    pack: "school",
    status: "planned",
    title: "School operations",
    description: "Students, attendance, exams, fees, guardian communication, and results."
  }
];
