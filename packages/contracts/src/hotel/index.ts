export interface HotelPropertyDto {
  id: string;
  tenantId: string;
  name: string;
  code: string;
  city: string;
  country: string;
  timezone: string;
  createdAt?: string;
}

export interface HotelRoomTypeDto {
  id: string;
  tenantId?: string;
  propertyId: string;
  name: string;
  code: string;
  category?: string;
  bedType?: string;
  occupancy: number;
  roomSizeSqm?: number;
  baseRateMinor: number;
  extraBedPriceMinor?: number;
  refundable?: boolean;
  currency: string;
  amenityIds?: string[];
  createdAt?: string;
}

export interface HotelRoomDto {
  id: string;
  tenantId?: string;
  propertyId: string;
  roomTypeId: string;
  roomNumber: string;
  status: "available" | "occupied" | "maintenance" | "dirty" | "blocked";
  occupancyStatus?: "vacant" | "occupied";
  housekeepingStatus?: "clean" | "dirty" | "inspected" | "dnd";
  sellStatus?: "sellable" | "blocked" | "maintenance" | "out_of_order";
  isActive?: boolean;
  featureTags?: string[];
  notes?: string;
  lastCleanedAt?: string;
  floorLabel?: string;
  createdAt?: string;
}

export interface HotelMealPlanDto {
  id: string;
  tenantId: string;
  propertyId: string;
  code: string;
  name: string;
  description?: string;
  pricePerPersonPerNightMinor: number;
  currency: string;
  includedMeals: string[];
  isActive: boolean;
  createdAt?: string;
}

export interface HotelGuestProfileDto {
  id: string;
  tenantId: string;
  firstName: string;
  lastName: string;
  fullName: string;
  email: string;
  phone: string;
  nationality?: string;
  loyaltyTier?: string;
  vip: boolean;
  preferredRoomTypeId?: string;
  dietaryPreference?: string;
  companyName?: string;
  identityDocumentNumber?: string;
  notes?: string;
  createdAt?: string;
}

export interface HotelSeasonalRateOverrideDto {
  seasonName: string;
  startDate: string;
  endDate: string;
  priceMinor: number;
}

export interface HotelRatePlanDto {
  id: string;
  tenantId: string;
  propertyId: string;
  roomTypeId: string;
  label: string;
  currency: string;
  weekendEnabled: boolean;
  weekendRateMinor?: number;
  seasonalOverrides: HotelSeasonalRateOverrideDto[];
  isActive: boolean;
  createdAt?: string;
}

export interface HotelAvailabilityRuleDto {
  id: string;
  tenantId: string;
  propertyId: string;
  roomTypeId: string;
  totalUnits: number;
  availableUnitsSnapshot?: number;
  minimumStayNights: number;
  maximumStayNights: number;
  blackoutDates: string[];
  isActive: boolean;
  createdAt?: string;
}

export interface HotelReservationDto {
  id: string;
  tenantId: string;
  propertyId: string;
  roomTypeId: string;
  roomId?: string;
  mealPlanId?: string;
  bookingReference?: string;
  bookingSource?: string;
  guestCustomerId: string;
  guestName?: string;
  checkInDate: string;
  checkOutDate: string;
  status: "pending" | "reserved" | "checked_in" | "checked_out" | "cancelled" | "no_show";
  specialRequests?: string;
  earlyCheckIn?: boolean;
  lateCheckOut?: boolean;
  actualCheckInAt?: string;
  actualCheckOutAt?: string;
  totalAmountMinor?: number;
  currency?: string;
  adults?: number;
  children?: number;
  createdAt?: string;
}

export interface HotelRoomMoveDto {
  id: string;
  tenantId: string;
  propertyId: string;
  stayId: string;
  reservationId: string;
  fromRoomId: string;
  toRoomId: string;
  movedAt: string;
  reason: string;
  movedByUserId: string;
  createdAt?: string;
}

export interface HotelStayDto {
  id: string;
  tenantId: string;
  propertyId: string;
  reservationId: string;
  roomTypeId: string;
  roomId: string;
  guestCustomerId: string;
  guestName?: string;
  status: "in_house" | "checked_out";
  checkedInAt: string;
  checkedOutAt?: string;
  notes?: string;
  roomMoves?: HotelRoomMoveDto[] | null;
  createdAt?: string;
}

export interface HotelGuestDocumentDto {
  id: string;
  tenantId: string;
  guestProfileId: string;
  documentKind: "passport" | "national_id" | "drivers_license" | "visa" | "other";
  documentNumber: string;
  issuingCountry?: string;
  expiresOn?: string;
  verificationStatus: "pending" | "verified" | "rejected";
  storageKey?: string;
  notes?: string;
  createdAt?: string;
}

export interface HotelFolioChargeDto {
  id: string;
  tenantId: string;
  folioId: string;
  reservationId: string;
  category:
    | "reservation_base"
    | "room_revenue"
    | "meal_plan"
    | "tax"
    | "fee"
    | "add_on"
    | "incidental"
    | "discount";
  label: string;
  serviceDate: string;
  quantity: number;
  unitAmountMinor: number;
  lineAmountMinor: number;
  taxAmountMinor: number;
  grossAmountMinor: number;
  notes?: string;
  createdByUserId: string;
  createdAt?: string;
}

export interface HotelPaymentDto {
  id: string;
  tenantId: string;
  propertyId: string;
  folioId: string;
  reservationId: string;
  amountMinor: number;
  currency: string;
  paymentMethod: "cash" | "card" | "upi" | "bank_transfer" | "wallet" | "other";
  status: "posted";
  reference?: string;
  notes?: string;
  receivedAt: string;
  recordedByUserId: string;
  createdAt?: string;
}

export interface HotelRefundDto {
  id: string;
  tenantId: string;
  propertyId: string;
  folioId: string;
  paymentId: string;
  reservationId: string;
  amountMinor: number;
  currency: string;
  reason: string;
  reference?: string;
  status: "processed";
  refundedAt: string;
  recordedByUserId: string;
  createdAt?: string;
}

export interface HotelFolioDto {
  id: string;
  tenantId: string;
  propertyId: string;
  reservationId: string;
  guestCustomerId: string;
  guestName?: string;
  status: "open" | "closed" | "invoiced";
  currency: string;
  subtotalMinor: number;
  taxMinor: number;
  totalMinor: number;
  paidMinor: number;
  balanceMinor: number;
  invoiceNumber?: string;
  invoiceIssuedAt?: string;
  closedAt?: string;
  charges?: HotelFolioChargeDto[] | null;
  payments?: HotelPaymentDto[] | null;
  refunds?: HotelRefundDto[] | null;
  createdAt?: string;
}

export interface HotelStaffMemberDto {
  id: string;
  tenantId: string;
  propertyId: string;
  staffCode: string;
  firstName: string;
  lastName: string;
  fullName: string;
  role: string;
  department: string;
  phone?: string;
  email?: string;
  employmentStatus: "active" | "inactive" | "notice";
  isActive: boolean;
  createdAt?: string;
}

export interface HotelShiftDto {
  id: string;
  tenantId: string;
  propertyId: string;
  staffMemberId: string;
  shiftDate: string;
  shiftKind: "morning" | "evening" | "night" | "general";
  startTime: string;
  endTime: string;
  status: "scheduled" | "checked_in" | "completed" | "missed";
  notes?: string;
  createdAt?: string;
}

export interface HotelNightAuditDto {
  id: string;
  tenantId: string;
  propertyId: string;
  auditDate: string;
  status: "completed" | "attention_required";
  report: Record<string, unknown>;
  completedAt: string;
  completedByUserId: string;
  createdAt?: string;
}

export interface HotelPropertyProfileDocumentDto {
  propertyId: string;
  brandName: string;
  heroTitle: string;
  heroSummary?: string;
  description?: string;
  addressLine1?: string;
  addressLine2?: string;
  city?: string;
  state?: string;
  country?: string;
  postalCode?: string;
  contactPhone?: string;
  contactEmail?: string;
  website?: string;
  checkInTime?: string;
  checkOutTime?: string;
  starRating?: number | null;
  highlights: string[];
  galleryUrls: string[];
  policies: string[];
  updatedAt?: string;
}

export interface HotelAmenityEntryDto {
  id: string;
  label: string;
  icon?: string;
  description?: string;
}

export interface HotelAmenityCategoryDto {
  key: string;
  label: string;
  amenities: HotelAmenityEntryDto[];
}

export interface HotelAmenityCatalogDocumentDto {
  propertyId: string;
  categories: HotelAmenityCategoryDto[];
  updatedAt?: string;
}

export interface HotelNearbyPlaceDto {
  name: string;
  kind: string;
  distanceKm: number;
  travelMinutes: number;
  summary?: string;
}

export interface HotelNearbyPlacesDocumentDto {
  propertyId: string;
  places: HotelNearbyPlaceDto[];
  updatedAt?: string;
}

export interface HotelInventoryCalendarDto {
  propertyId: string;
  roomTypeId: string;
  date: string;
  availableUnits: number;
  soldUnits: number;
  blockedUnits: number;
}

export interface HotelHousekeepingTaskDto {
  id: string;
  tenantId: string;
  propertyId: string;
  roomId: string;
  status: "pending" | "in_progress" | "completed";
  priority: "low" | "medium" | "high";
  notes?: string;
  assignedStaffId?: string;
  assignedTo?: string;
  createdAt?: string;
}

export interface HotelMaintenanceTicketDto {
  id: string;
  tenantId: string;
  propertyId: string;
  roomId?: string;
  title: string;
  description?: string;
  status: "open" | "in_progress" | "resolved" | "cancelled";
  priority: "low" | "medium" | "high" | "critical";
  assignedStaffId?: string;
  assignedTo?: string;
  createdAt?: string;
}
