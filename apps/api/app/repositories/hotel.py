from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import (
    HotelFolioChargeModel,
    HotelFolioModel,
    HotelAvailabilityRuleModel,
    HotelGuestDocumentModel,
    HotelGuestProfileModel,
    HotelHousekeepingTaskModel,
    HotelMaintenanceTicketModel,
    HotelMealPlanModel,
    HotelNightAuditModel,
    HotelPaymentModel,
    HotelPropertyModel,
    HotelRatePlanModel,
    HotelReservationModel,
    HotelRefundModel,
    HotelRoomMoveModel,
    HotelRoomModel,
    HotelRoomTypeModel,
    HotelShiftModel,
    HotelStaffMemberModel,
    HotelStayModel,
)


def list_properties(db: Session, *, tenant_id: str) -> list[HotelPropertyModel]:
    query = select(HotelPropertyModel).where(HotelPropertyModel.tenant_id == tenant_id)
    query = query.order_by(HotelPropertyModel.created_at.desc())
    return list(db.scalars(query))


def get_property(db: Session, *, tenant_id: str, property_id: str) -> HotelPropertyModel | None:
    query = select(HotelPropertyModel).where(
        HotelPropertyModel.tenant_id == tenant_id,
        HotelPropertyModel.id == property_id,
    )
    return db.scalar(query)


def find_property_by_code(db: Session, *, tenant_id: str, code: str) -> HotelPropertyModel | None:
    query = select(HotelPropertyModel).where(
        HotelPropertyModel.tenant_id == tenant_id,
        HotelPropertyModel.code == code,
    )
    return db.scalar(query)


def create_property(
    db: Session,
    *,
    tenant_id: str,
    name: str,
    code: str,
    city: str,
    country: str,
    timezone: str,
) -> HotelPropertyModel:
    model = HotelPropertyModel(
        tenant_id=tenant_id,
        name=name,
        code=code,
        city=city,
        country=country,
        timezone=timezone,
    )
    db.add(model)
    db.flush()
    return model


def list_room_types(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
) -> list[HotelRoomTypeModel]:
    query = select(HotelRoomTypeModel).where(HotelRoomTypeModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelRoomTypeModel.property_id == property_id)
    query = query.order_by(HotelRoomTypeModel.created_at.desc())
    return list(db.scalars(query))


def get_room_type(db: Session, *, tenant_id: str, room_type_id: str) -> HotelRoomTypeModel | None:
    query = select(HotelRoomTypeModel).where(
        HotelRoomTypeModel.tenant_id == tenant_id,
        HotelRoomTypeModel.id == room_type_id,
    )
    return db.scalar(query)


def find_room_type_by_code(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    code: str,
) -> HotelRoomTypeModel | None:
    query = select(HotelRoomTypeModel).where(
        HotelRoomTypeModel.tenant_id == tenant_id,
        HotelRoomTypeModel.property_id == property_id,
        HotelRoomTypeModel.code == code,
    )
    return db.scalar(query)


def create_room_type(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    name: str,
    code: str,
    category: str | None,
    bed_type: str | None,
    occupancy: int,
    room_size_sqm: int | None,
    base_rate_minor: int,
    extra_bed_price_minor: int,
    refundable: bool,
    currency: str,
    amenity_ids: list[str],
) -> HotelRoomTypeModel:
    model = HotelRoomTypeModel(
        tenant_id=tenant_id,
        property_id=property_id,
        name=name,
        code=code,
        category=category,
        bed_type=bed_type,
        occupancy=occupancy,
        room_size_sqm=room_size_sqm,
        base_rate_minor=base_rate_minor,
        extra_bed_price_minor=extra_bed_price_minor,
        refundable=refundable,
        currency=currency,
        amenity_ids=amenity_ids,
    )
    db.add(model)
    db.flush()
    return model


def list_rooms(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
) -> list[HotelRoomModel]:
    query = select(HotelRoomModel).where(HotelRoomModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelRoomModel.property_id == property_id)
    query = query.order_by(HotelRoomModel.created_at.desc())
    return list(db.scalars(query))


def get_room(db: Session, *, tenant_id: str, room_id: str) -> HotelRoomModel | None:
    query = select(HotelRoomModel).where(
        HotelRoomModel.tenant_id == tenant_id,
        HotelRoomModel.id == room_id,
    )
    return db.scalar(query)


def find_room_by_number(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_number: str,
) -> HotelRoomModel | None:
    query = select(HotelRoomModel).where(
        HotelRoomModel.tenant_id == tenant_id,
        HotelRoomModel.property_id == property_id,
        HotelRoomModel.room_number == room_number,
    )
    return db.scalar(query)


def create_room(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_type_id: str,
    room_number: str,
    status: str,
    occupancy_status: str,
    housekeeping_status: str,
    sell_status: str,
    is_active: bool,
    feature_tags: list[str],
    notes: str | None,
    last_cleaned_at: str | None,
    floor_label: str | None,
) -> HotelRoomModel:
    model = HotelRoomModel(
        tenant_id=tenant_id,
        property_id=property_id,
        room_type_id=room_type_id,
        room_number=room_number,
        status=status,
        occupancy_status=occupancy_status,
        housekeeping_status=housekeeping_status,
        sell_status=sell_status,
        is_active=is_active,
        feature_tags=feature_tags,
        notes=notes,
        last_cleaned_at=last_cleaned_at,
        floor_label=floor_label,
    )
    db.add(model)
    db.flush()
    return model


def list_meal_plans(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
) -> list[HotelMealPlanModel]:
    query = select(HotelMealPlanModel).where(HotelMealPlanModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelMealPlanModel.property_id == property_id)
    query = query.order_by(HotelMealPlanModel.created_at.desc())
    return list(db.scalars(query))


def get_meal_plan(db: Session, *, tenant_id: str, meal_plan_id: str) -> HotelMealPlanModel | None:
    query = select(HotelMealPlanModel).where(
        HotelMealPlanModel.tenant_id == tenant_id,
        HotelMealPlanModel.id == meal_plan_id,
    )
    return db.scalar(query)


def find_meal_plan_by_code(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    code: str,
) -> HotelMealPlanModel | None:
    query = select(HotelMealPlanModel).where(
        HotelMealPlanModel.tenant_id == tenant_id,
        HotelMealPlanModel.property_id == property_id,
        HotelMealPlanModel.code == code,
    )
    return db.scalar(query)


def create_meal_plan(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    code: str,
    name: str,
    description: str | None,
    price_per_person_per_night_minor: int,
    currency: str,
    included_meals: list[str],
    is_active: bool,
) -> HotelMealPlanModel:
    model = HotelMealPlanModel(
        tenant_id=tenant_id,
        property_id=property_id,
        code=code,
        name=name,
        description=description,
        price_per_person_per_night_minor=price_per_person_per_night_minor,
        currency=currency,
        included_meals=included_meals,
        is_active=is_active,
    )
    db.add(model)
    db.flush()
    return model


def list_guest_profiles(db: Session, *, tenant_id: str) -> list[HotelGuestProfileModel]:
    query = select(HotelGuestProfileModel).where(HotelGuestProfileModel.tenant_id == tenant_id)
    query = query.order_by(HotelGuestProfileModel.created_at.desc())
    return list(db.scalars(query))


def get_guest_profile(db: Session, *, tenant_id: str, guest_profile_id: str) -> HotelGuestProfileModel | None:
    query = select(HotelGuestProfileModel).where(
        HotelGuestProfileModel.tenant_id == tenant_id,
        HotelGuestProfileModel.id == guest_profile_id,
    )
    return db.scalar(query)


def list_guest_documents(db: Session, *, tenant_id: str, guest_profile_id: str) -> list[HotelGuestDocumentModel]:
    query = select(HotelGuestDocumentModel).where(
        HotelGuestDocumentModel.tenant_id == tenant_id,
        HotelGuestDocumentModel.guest_profile_id == guest_profile_id,
    )
    query = query.order_by(HotelGuestDocumentModel.created_at.desc())
    return list(db.scalars(query))


def create_guest_document(
    db: Session,
    *,
    tenant_id: str,
    guest_profile_id: str,
    document_kind: str,
    document_number: str,
    issuing_country: str | None,
    expires_on: date | None,
    verification_status: str,
    storage_key: str | None,
    notes: str | None,
) -> HotelGuestDocumentModel:
    model = HotelGuestDocumentModel(
        tenant_id=tenant_id,
        guest_profile_id=guest_profile_id,
        document_kind=document_kind,
        document_number=document_number,
        issuing_country=issuing_country,
        expires_on=expires_on,
        verification_status=verification_status,
        storage_key=storage_key,
        notes=notes,
    )
    db.add(model)
    db.flush()
    return model


def find_guest_profile_by_email(db: Session, *, tenant_id: str, email: str) -> HotelGuestProfileModel | None:
    query = select(HotelGuestProfileModel).where(
        HotelGuestProfileModel.tenant_id == tenant_id,
        HotelGuestProfileModel.email == email,
    )
    return db.scalar(query)


def create_guest_profile(
    db: Session,
    *,
    tenant_id: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    nationality: str | None,
    loyalty_tier: str | None,
    vip: bool,
    preferred_room_type_id: str | None,
    dietary_preference: str | None,
    company_name: str | None,
    identity_document_number: str | None,
    notes: str | None,
) -> HotelGuestProfileModel:
    model = HotelGuestProfileModel(
        tenant_id=tenant_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        nationality=nationality,
        loyalty_tier=loyalty_tier,
        vip=vip,
        preferred_room_type_id=preferred_room_type_id,
        dietary_preference=dietary_preference,
        company_name=company_name,
        identity_document_number=identity_document_number,
        notes=notes,
    )
    db.add(model)
    db.flush()
    return model


def list_rate_plans(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    room_type_id: str | None = None,
) -> list[HotelRatePlanModel]:
    query = select(HotelRatePlanModel).where(HotelRatePlanModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelRatePlanModel.property_id == property_id)
    if room_type_id:
        query = query.where(HotelRatePlanModel.room_type_id == room_type_id)
    query = query.order_by(HotelRatePlanModel.created_at.desc())
    return list(db.scalars(query))


def find_rate_plan_by_label(
    db: Session,
    *,
    tenant_id: str,
    room_type_id: str,
    label: str,
) -> HotelRatePlanModel | None:
    query = select(HotelRatePlanModel).where(
        HotelRatePlanModel.tenant_id == tenant_id,
        HotelRatePlanModel.room_type_id == room_type_id,
        HotelRatePlanModel.label == label,
    )
    return db.scalar(query)


def create_rate_plan(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_type_id: str,
    label: str,
    currency: str,
    weekend_enabled: bool,
    weekend_rate_minor: int | None,
    seasonal_overrides: list[dict[str, object]],
    is_active: bool,
) -> HotelRatePlanModel:
    model = HotelRatePlanModel(
        tenant_id=tenant_id,
        property_id=property_id,
        room_type_id=room_type_id,
        label=label,
        currency=currency,
        weekend_enabled=weekend_enabled,
        weekend_rate_minor=weekend_rate_minor,
        seasonal_overrides=seasonal_overrides,
        is_active=is_active,
    )
    db.add(model)
    db.flush()
    return model


def list_availability_rules(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    room_type_id: str | None = None,
) -> list[HotelAvailabilityRuleModel]:
    query = select(HotelAvailabilityRuleModel).where(HotelAvailabilityRuleModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelAvailabilityRuleModel.property_id == property_id)
    if room_type_id:
        query = query.where(HotelAvailabilityRuleModel.room_type_id == room_type_id)
    query = query.order_by(HotelAvailabilityRuleModel.created_at.desc())
    return list(db.scalars(query))


def get_availability_rule(db: Session, *, tenant_id: str, availability_rule_id: str) -> HotelAvailabilityRuleModel | None:
    query = select(HotelAvailabilityRuleModel).where(
        HotelAvailabilityRuleModel.tenant_id == tenant_id,
        HotelAvailabilityRuleModel.id == availability_rule_id,
    )
    return db.scalar(query)


def find_availability_rule_by_room_type(
    db: Session,
    *,
    tenant_id: str,
    room_type_id: str,
) -> HotelAvailabilityRuleModel | None:
    query = select(HotelAvailabilityRuleModel).where(
        HotelAvailabilityRuleModel.tenant_id == tenant_id,
        HotelAvailabilityRuleModel.room_type_id == room_type_id,
    )
    return db.scalar(query)


def create_availability_rule(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_type_id: str,
    total_units: int,
    available_units_snapshot: int | None,
    minimum_stay_nights: int,
    maximum_stay_nights: int,
    blackout_dates: list[str],
    is_active: bool,
) -> HotelAvailabilityRuleModel:
    model = HotelAvailabilityRuleModel(
        tenant_id=tenant_id,
        property_id=property_id,
        room_type_id=room_type_id,
        total_units=total_units,
        available_units_snapshot=available_units_snapshot,
        minimum_stay_nights=minimum_stay_nights,
        maximum_stay_nights=maximum_stay_nights,
        blackout_dates=blackout_dates,
        is_active=is_active,
    )
    db.add(model)
    db.flush()
    return model


def list_reservations(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    status: str | None = None,
) -> list[HotelReservationModel]:
    query = select(HotelReservationModel).where(HotelReservationModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelReservationModel.property_id == property_id)
    if status:
        query = query.where(HotelReservationModel.status == status)
    query = query.order_by(HotelReservationModel.created_at.desc())
    return list(db.scalars(query))


def get_reservation(db: Session, *, tenant_id: str, reservation_id: str) -> HotelReservationModel | None:
    query = select(HotelReservationModel).where(
        HotelReservationModel.tenant_id == tenant_id,
        HotelReservationModel.id == reservation_id,
    )
    return db.scalar(query)


def list_stays(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    status: str | None = None,
) -> list[HotelStayModel]:
    query = select(HotelStayModel).where(HotelStayModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelStayModel.property_id == property_id)
    if status:
        query = query.where(HotelStayModel.status == status)
    query = query.order_by(HotelStayModel.created_at.desc())
    return list(db.scalars(query))


def get_stay(db: Session, *, tenant_id: str, stay_id: str) -> HotelStayModel | None:
    query = select(HotelStayModel).where(
        HotelStayModel.tenant_id == tenant_id,
        HotelStayModel.id == stay_id,
    )
    return db.scalar(query)


def find_stay_by_reservation(db: Session, *, tenant_id: str, reservation_id: str) -> HotelStayModel | None:
    query = select(HotelStayModel).where(
        HotelStayModel.tenant_id == tenant_id,
        HotelStayModel.reservation_id == reservation_id,
    )
    return db.scalar(query)


def create_stay(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    reservation_id: str,
    room_type_id: str,
    room_id: str,
    guest_customer_id: str,
    guest_name: str | None,
    status: str,
    checked_in_at: str,
    checked_out_at: str | None,
    notes: str | None,
) -> HotelStayModel:
    model = HotelStayModel(
        tenant_id=tenant_id,
        property_id=property_id,
        reservation_id=reservation_id,
        room_type_id=room_type_id,
        room_id=room_id,
        guest_customer_id=guest_customer_id,
        guest_name=guest_name,
        status=status,
        checked_in_at=checked_in_at,
        checked_out_at=checked_out_at,
        notes=notes,
    )
    db.add(model)
    db.flush()
    return model


def list_room_moves(db: Session, *, tenant_id: str, stay_id: str) -> list[HotelRoomMoveModel]:
    query = select(HotelRoomMoveModel).where(
        HotelRoomMoveModel.tenant_id == tenant_id,
        HotelRoomMoveModel.stay_id == stay_id,
    )
    query = query.order_by(HotelRoomMoveModel.created_at.asc())
    return list(db.scalars(query))


def create_room_move(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    stay_id: str,
    reservation_id: str,
    from_room_id: str,
    to_room_id: str,
    moved_at: str,
    reason: str,
    moved_by_user_id: str,
) -> HotelRoomMoveModel:
    model = HotelRoomMoveModel(
        tenant_id=tenant_id,
        property_id=property_id,
        stay_id=stay_id,
        reservation_id=reservation_id,
        from_room_id=from_room_id,
        to_room_id=to_room_id,
        moved_at=moved_at,
        reason=reason,
        moved_by_user_id=moved_by_user_id,
    )
    db.add(model)
    db.flush()
    return model


def create_reservation(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_type_id: str,
    room_id: str | None,
    meal_plan_id: str | None,
    booking_reference: str | None,
    booking_source: str | None,
    guest_customer_id: str,
    guest_name: str | None,
    check_in_date: date,
    check_out_date: date,
    status: str,
    special_requests: str | None,
    early_check_in: bool,
    late_check_out: bool,
    actual_check_in_at: str | None,
    actual_check_out_at: str | None,
    total_amount_minor: int,
    currency: str,
    adults: int,
    children: int,
) -> HotelReservationModel:
    model = HotelReservationModel(
        tenant_id=tenant_id,
        property_id=property_id,
        room_type_id=room_type_id,
        room_id=room_id,
        meal_plan_id=meal_plan_id,
        booking_reference=booking_reference,
        booking_source=booking_source,
        guest_customer_id=guest_customer_id,
        guest_name=guest_name,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        status=status,
        special_requests=special_requests,
        early_check_in=early_check_in,
        late_check_out=late_check_out,
        actual_check_in_at=actual_check_in_at,
        actual_check_out_at=actual_check_out_at,
        total_amount_minor=total_amount_minor,
        currency=currency,
        adults=adults,
        children=children,
    )
    db.add(model)
    db.flush()
    return model


def find_conflicting_reservation(
    db: Session,
    *,
    tenant_id: str,
    room_id: str,
    check_in_date: date,
    check_out_date: date,
    exclude_reservation_id: str | None = None,
) -> HotelReservationModel | None:
    query = select(HotelReservationModel).where(
        HotelReservationModel.tenant_id == tenant_id,
        HotelReservationModel.room_id == room_id,
        HotelReservationModel.status.in_(["reserved", "checked_in"]),
        HotelReservationModel.check_in_date < check_out_date,
        HotelReservationModel.check_out_date > check_in_date,
    )
    if exclude_reservation_id:
        query = query.where(HotelReservationModel.id != exclude_reservation_id)
    return db.scalar(query)


def list_folios(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    reservation_id: str | None = None,
    status: str | None = None,
) -> list[HotelFolioModel]:
    query = select(HotelFolioModel).where(HotelFolioModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelFolioModel.property_id == property_id)
    if reservation_id:
        query = query.where(HotelFolioModel.reservation_id == reservation_id)
    if status:
        query = query.where(HotelFolioModel.status == status)
    query = query.order_by(HotelFolioModel.created_at.desc())
    return list(db.scalars(query))


def get_folio(db: Session, *, tenant_id: str, folio_id: str) -> HotelFolioModel | None:
    query = select(HotelFolioModel).where(
        HotelFolioModel.tenant_id == tenant_id,
        HotelFolioModel.id == folio_id,
    )
    return db.scalar(query)


def find_folio_by_reservation(db: Session, *, tenant_id: str, reservation_id: str) -> HotelFolioModel | None:
    query = select(HotelFolioModel).where(
        HotelFolioModel.tenant_id == tenant_id,
        HotelFolioModel.reservation_id == reservation_id,
    )
    return db.scalar(query)


def create_folio(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    reservation_id: str,
    guest_customer_id: str,
    guest_name: str | None,
    status: str,
    currency: str,
    subtotal_minor: int,
    tax_minor: int,
    total_minor: int,
    paid_minor: int,
    balance_minor: int,
    invoice_number: str | None,
    invoice_issued_at: str | None,
    closed_at: str | None,
) -> HotelFolioModel:
    model = HotelFolioModel(
        tenant_id=tenant_id,
        property_id=property_id,
        reservation_id=reservation_id,
        guest_customer_id=guest_customer_id,
        guest_name=guest_name,
        status=status,
        currency=currency,
        subtotal_minor=subtotal_minor,
        tax_minor=tax_minor,
        total_minor=total_minor,
        paid_minor=paid_minor,
        balance_minor=balance_minor,
        invoice_number=invoice_number,
        invoice_issued_at=invoice_issued_at,
        closed_at=closed_at,
    )
    db.add(model)
    db.flush()
    return model


def list_folio_charges(
    db: Session,
    *,
    tenant_id: str,
    folio_id: str,
) -> list[HotelFolioChargeModel]:
    query = select(HotelFolioChargeModel).where(
        HotelFolioChargeModel.tenant_id == tenant_id,
        HotelFolioChargeModel.folio_id == folio_id,
    )
    query = query.order_by(HotelFolioChargeModel.service_date.asc(), HotelFolioChargeModel.created_at.asc())
    return list(db.scalars(query))


def create_folio_charge(
    db: Session,
    *,
    tenant_id: str,
    folio_id: str,
    reservation_id: str,
    category: str,
    label: str,
    service_date: date,
    quantity: int,
    unit_amount_minor: int,
    line_amount_minor: int,
    tax_amount_minor: int,
    notes: str | None,
    created_by_user_id: str,
) -> HotelFolioChargeModel:
    model = HotelFolioChargeModel(
        tenant_id=tenant_id,
        folio_id=folio_id,
        reservation_id=reservation_id,
        category=category,
        label=label,
        service_date=service_date,
        quantity=quantity,
        unit_amount_minor=unit_amount_minor,
        line_amount_minor=line_amount_minor,
        tax_amount_minor=tax_amount_minor,
        notes=notes,
        created_by_user_id=created_by_user_id,
    )
    db.add(model)
    db.flush()
    return model


def list_payments(
    db: Session,
    *,
    tenant_id: str,
    folio_id: str | None = None,
    property_id: str | None = None,
) -> list[HotelPaymentModel]:
    query = select(HotelPaymentModel).where(HotelPaymentModel.tenant_id == tenant_id)
    if folio_id:
        query = query.where(HotelPaymentModel.folio_id == folio_id)
    if property_id:
        query = query.where(HotelPaymentModel.property_id == property_id)
    query = query.order_by(HotelPaymentModel.created_at.desc())
    return list(db.scalars(query))


def get_payment(db: Session, *, tenant_id: str, payment_id: str) -> HotelPaymentModel | None:
    query = select(HotelPaymentModel).where(
        HotelPaymentModel.tenant_id == tenant_id,
        HotelPaymentModel.id == payment_id,
    )
    return db.scalar(query)


def create_payment(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    folio_id: str,
    reservation_id: str,
    amount_minor: int,
    currency: str,
    payment_method: str,
    status: str,
    reference: str | None,
    notes: str | None,
    received_at: str,
    recorded_by_user_id: str,
) -> HotelPaymentModel:
    model = HotelPaymentModel(
        tenant_id=tenant_id,
        property_id=property_id,
        folio_id=folio_id,
        reservation_id=reservation_id,
        amount_minor=amount_minor,
        currency=currency,
        payment_method=payment_method,
        status=status,
        reference=reference,
        notes=notes,
        received_at=received_at,
        recorded_by_user_id=recorded_by_user_id,
    )
    db.add(model)
    db.flush()
    return model


def list_refunds(
    db: Session,
    *,
    tenant_id: str,
    folio_id: str | None = None,
    property_id: str | None = None,
) -> list[HotelRefundModel]:
    query = select(HotelRefundModel).where(HotelRefundModel.tenant_id == tenant_id)
    if folio_id:
        query = query.where(HotelRefundModel.folio_id == folio_id)
    if property_id:
        query = query.where(HotelRefundModel.property_id == property_id)
    query = query.order_by(HotelRefundModel.created_at.desc())
    return list(db.scalars(query))


def create_refund(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    folio_id: str,
    payment_id: str,
    reservation_id: str,
    amount_minor: int,
    currency: str,
    reason: str,
    reference: str | None,
    status: str,
    refunded_at: str,
    recorded_by_user_id: str,
) -> HotelRefundModel:
    model = HotelRefundModel(
        tenant_id=tenant_id,
        property_id=property_id,
        folio_id=folio_id,
        payment_id=payment_id,
        reservation_id=reservation_id,
        amount_minor=amount_minor,
        currency=currency,
        reason=reason,
        reference=reference,
        status=status,
        refunded_at=refunded_at,
        recorded_by_user_id=recorded_by_user_id,
    )
    db.add(model)
    db.flush()
    return model


def list_staff_members(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
) -> list[HotelStaffMemberModel]:
    query = select(HotelStaffMemberModel).where(HotelStaffMemberModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelStaffMemberModel.property_id == property_id)
    query = query.order_by(HotelStaffMemberModel.created_at.desc())
    return list(db.scalars(query))


def get_staff_member(db: Session, *, tenant_id: str, staff_member_id: str) -> HotelStaffMemberModel | None:
    query = select(HotelStaffMemberModel).where(
        HotelStaffMemberModel.tenant_id == tenant_id,
        HotelStaffMemberModel.id == staff_member_id,
    )
    return db.scalar(query)


def find_staff_member_by_code(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    staff_code: str,
) -> HotelStaffMemberModel | None:
    query = select(HotelStaffMemberModel).where(
        HotelStaffMemberModel.tenant_id == tenant_id,
        HotelStaffMemberModel.property_id == property_id,
        HotelStaffMemberModel.staff_code == staff_code,
    )
    return db.scalar(query)


def create_staff_member(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    staff_code: str,
    first_name: str,
    last_name: str,
    role: str,
    department: str,
    phone: str | None,
    email: str | None,
    employment_status: str,
    is_active: bool,
) -> HotelStaffMemberModel:
    model = HotelStaffMemberModel(
        tenant_id=tenant_id,
        property_id=property_id,
        staff_code=staff_code,
        first_name=first_name,
        last_name=last_name,
        role=role,
        department=department,
        phone=phone,
        email=email,
        employment_status=employment_status,
        is_active=is_active,
    )
    db.add(model)
    db.flush()
    return model


def list_shifts(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    staff_member_id: str | None = None,
    shift_date: date | None = None,
) -> list[HotelShiftModel]:
    query = select(HotelShiftModel).where(HotelShiftModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelShiftModel.property_id == property_id)
    if staff_member_id:
        query = query.where(HotelShiftModel.staff_member_id == staff_member_id)
    if shift_date:
        query = query.where(HotelShiftModel.shift_date == shift_date)
    query = query.order_by(HotelShiftModel.shift_date.desc(), HotelShiftModel.created_at.desc())
    return list(db.scalars(query))


def create_shift(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    staff_member_id: str,
    shift_date: date,
    shift_kind: str,
    start_time: str,
    end_time: str,
    status: str,
    notes: str | None,
) -> HotelShiftModel:
    model = HotelShiftModel(
        tenant_id=tenant_id,
        property_id=property_id,
        staff_member_id=staff_member_id,
        shift_date=shift_date,
        shift_kind=shift_kind,
        start_time=start_time,
        end_time=end_time,
        status=status,
        notes=notes,
    )
    db.add(model)
    db.flush()
    return model


def list_night_audits(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
) -> list[HotelNightAuditModel]:
    query = select(HotelNightAuditModel).where(HotelNightAuditModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelNightAuditModel.property_id == property_id)
    query = query.order_by(HotelNightAuditModel.audit_date.desc(), HotelNightAuditModel.created_at.desc())
    return list(db.scalars(query))


def find_night_audit_by_date(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    audit_date: date,
) -> HotelNightAuditModel | None:
    query = select(HotelNightAuditModel).where(
        HotelNightAuditModel.tenant_id == tenant_id,
        HotelNightAuditModel.property_id == property_id,
        HotelNightAuditModel.audit_date == audit_date,
    )
    return db.scalar(query)


def create_night_audit(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    audit_date: date,
    status: str,
    report_json: dict[str, object],
    completed_at: str,
    completed_by_user_id: str,
) -> HotelNightAuditModel:
    model = HotelNightAuditModel(
        tenant_id=tenant_id,
        property_id=property_id,
        audit_date=audit_date,
        status=status,
        report_json=report_json,
        completed_at=completed_at,
        completed_by_user_id=completed_by_user_id,
    )
    db.add(model)
    db.flush()
    return model


def list_housekeeping_tasks(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    status: str | None = None,
) -> list[HotelHousekeepingTaskModel]:
    query = select(HotelHousekeepingTaskModel).where(HotelHousekeepingTaskModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelHousekeepingTaskModel.property_id == property_id)
    if status:
        query = query.where(HotelHousekeepingTaskModel.status == status)
    query = query.order_by(HotelHousekeepingTaskModel.created_at.desc())
    return list(db.scalars(query))


def get_housekeeping_task(
    db: Session,
    *,
    tenant_id: str,
    task_id: str,
) -> HotelHousekeepingTaskModel | None:
    query = select(HotelHousekeepingTaskModel).where(
        HotelHousekeepingTaskModel.tenant_id == tenant_id,
        HotelHousekeepingTaskModel.id == task_id,
    )
    return db.scalar(query)


def find_open_housekeeping_task(
    db: Session,
    *,
    tenant_id: str,
    room_id: str,
) -> HotelHousekeepingTaskModel | None:
    query = select(HotelHousekeepingTaskModel).where(
        HotelHousekeepingTaskModel.tenant_id == tenant_id,
        HotelHousekeepingTaskModel.room_id == room_id,
        HotelHousekeepingTaskModel.status.in_(["pending", "in_progress"]),
    )
    return db.scalar(query)


def create_housekeeping_task(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_id: str,
    status: str,
    priority: str,
    notes: str | None,
    assigned_staff_id: str | None,
    assigned_to: str | None,
) -> HotelHousekeepingTaskModel:
    model = HotelHousekeepingTaskModel(
        tenant_id=tenant_id,
        property_id=property_id,
        room_id=room_id,
        status=status,
        priority=priority,
        notes=notes,
        assigned_staff_id=assigned_staff_id,
        assigned_to=assigned_to,
    )
    db.add(model)
    db.flush()
    return model


def list_maintenance_tickets(
    db: Session,
    *,
    tenant_id: str,
    property_id: str | None = None,
    status: str | None = None,
) -> list[HotelMaintenanceTicketModel]:
    query = select(HotelMaintenanceTicketModel).where(HotelMaintenanceTicketModel.tenant_id == tenant_id)
    if property_id:
        query = query.where(HotelMaintenanceTicketModel.property_id == property_id)
    if status:
        query = query.where(HotelMaintenanceTicketModel.status == status)
    query = query.order_by(HotelMaintenanceTicketModel.created_at.desc())
    return list(db.scalars(query))


def get_maintenance_ticket(
    db: Session,
    *,
    tenant_id: str,
    ticket_id: str,
) -> HotelMaintenanceTicketModel | None:
    query = select(HotelMaintenanceTicketModel).where(
        HotelMaintenanceTicketModel.tenant_id == tenant_id,
        HotelMaintenanceTicketModel.id == ticket_id,
    )
    return db.scalar(query)


def create_maintenance_ticket(
    db: Session,
    *,
    tenant_id: str,
    property_id: str,
    room_id: str | None,
    title: str,
    description: str | None,
    status: str,
    priority: str,
    assigned_staff_id: str | None,
    assigned_to: str | None,
) -> HotelMaintenanceTicketModel:
    model = HotelMaintenanceTicketModel(
        tenant_id=tenant_id,
        property_id=property_id,
        room_id=room_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        assigned_staff_id=assigned_staff_id,
        assigned_to=assigned_to,
    )
    db.add(model)
    db.flush()
    return model


def find_open_maintenance_tickets_for_room(
    db: Session,
    *,
    tenant_id: str,
    room_id: str,
) -> list[HotelMaintenanceTicketModel]:
    query = select(HotelMaintenanceTicketModel).where(
        HotelMaintenanceTicketModel.tenant_id == tenant_id,
        HotelMaintenanceTicketModel.room_id == room_id,
        HotelMaintenanceTicketModel.status.in_(["open", "in_progress"]),
    )
    return list(db.scalars(query))
