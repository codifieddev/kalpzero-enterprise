export interface TravelPackageDto {
  id: string;
  tenantId: string;
  code: string;
  slug: string;
  title: string;
  summary?: string;
  originCity: string;
  destinationCity: string;
  destinationCountry: string;
  durationDays: number;
  basePriceMinor: number;
  currency: string;
  status: "draft" | "active" | "archived";
  itineraryDays: ItineraryDayDto[];
}

export interface ItineraryDayDto {
  id: string;
  tenantId: string;
  packageId: string;
  dayNumber: number;
  title: string;
  summary: string;
  hotelRefId?: string;
  activityRefIds: string[];
  transferRefIds: string[];
}

export interface DepartureDto {
  id: string;
  tenantId: string;
  packageId: string;
  departureDate: string;
  returnDate: string;
  seatsTotal: number;
  seatsAvailable: number;
  priceOverrideMinor?: number;
  status: "scheduled" | "sold_out" | "closed";
}

export interface TravelerDto {
  id: string;
  tenantId: string;
  customerId: string;
  passportNumber?: string;
  nationality?: string;
}

export interface TravelLeadDto {
  id: string;
  tenantId: string;
  source: string;
  interestedPackageId?: string;
  departureId?: string;
  customerId?: string;
  contactName: string;
  contactPhone: string;
  travelersCount: number;
  desiredDepartureDate?: string;
  budgetMinor?: number;
  currency: string;
  notes?: string;
  status: "new" | "qualified" | "proposal_sent" | "won" | "lost";
}
