import re
from datetime import date
from uuid import uuid4
from typing import Any

from beanie.operators import In
from app.core.config import get_settings
from app.db.mongo import get_runtime_motor_database
from app.models.hotel import (
    HotelProperty,
    HotelRoomType,
    HotelRoom,
    HotelMealPlan,
    HotelGuestProfile,
    HotelRatePlan,
    HotelAvailabilityRule,
    HotelReservation,
    HotelStay,
    HotelRoomMove,
    HotelGuestDocument,
    HotelFolio,
    HotelFolioCharge,
    HotelPayment,
    HotelStaffMember,
    HotelShift,
    HotelNightAudit)


async def list_properties(db_name: str) -> list[dict[str, Any]]:
    properties = await HotelProperty.find().sort("-created_at").to_list()
    return [p.model_dump() for p in properties]


async def get_property(db_name: str, *, property_id: str) -> dict[str, Any] | None:
    prop = await HotelProperty.find_one(
        HotelProperty.id == property_id)
    return prop.model_dump() if prop else None


async def find_property_by_code(db_name: str, *, code: str) -> dict[str, Any] | None:
    prop = await HotelProperty.find_one(
        HotelProperty.code == code)
    return prop.model_dump() if prop else None


async def create_property(
    db_name: str,
    *,
    name: str,
    code: str,
    city: str,
    country: str,
    timezone: str) -> dict[str, Any]:
    model = HotelProperty(
        name=name,
        code=code,
        city=city,
        country=country,
        timezone=timezone)
    await model.insert()
    return model.model_dump()


async def list_room_types(
    db_name: str,
    *,
    property_id: str | None = None) -> list[dict[str, Any]]:
    query = HotelRoomType.find()
    if property_id:
        query = query.find(HotelRoomType.property_id == property_id),
    room_types = await query.sort("-created_at").to_list()
    return [rt.model_dump() for rt in room_types]


async def get_room_type(db_name: str, *, room_type_id: str) -> dict[str, Any] | None:
    rt = await HotelRoomType.find_one(
        HotelRoomType.id == room_type_id)
    return rt.model_dump() if rt else None


async def find_room_type_by_code(
    db_name: str,
    *,
    property_id: str,
    code: str) -> dict[str, Any] | None:
    rt = await HotelRoomType.find_one(
        HotelRoomType.property_id == property_id,
        HotelRoomType.code == code)
    return rt.model_dump() if rt else None


async def create_room_type(
    db_name: str,
    *,
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
    amenity_ids: list[str]) -> dict[str, Any]:
    model = HotelRoomType(
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
        amenity_ids=amenity_ids)
    await model.insert()
    return model.model_dump()


async def list_rooms(
    db_name: str,
    *,
    property_id: str | None = None) -> list[dict[str, Any]]:
    query = HotelRoom.find()
    if property_id:
        query = query.find(HotelRoom.property_id == property_id),
    rooms = await query.sort("-created_at").to_list()
    return [r.model_dump() for r in rooms]


async def get_room(db_name: str, *, room_id: str) -> dict[str, Any] | None:
    rm = await HotelRoom.find_one(
        HotelRoom.id == room_id)
    return rm.model_dump() if rm else None


async def find_room_by_number(
    db_name: str,
    *,
    property_id: str,
    room_number: str) -> dict[str, Any] | None:
    rm = await HotelRoom.find_one(
        HotelRoom.property_id == property_id,
        HotelRoom.room_number == room_number)
    return rm.model_dump() if rm else None


async def create_room(
    db_name: str,
    *,
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
    floor_label: str | None) -> dict[str, Any]:
    model = HotelRoom(
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
        floor_label=floor_label)
    await model.insert()
    return model.model_dump()


async def list_meal_plans(
    db_name: str,
    *,
    property_id: str | None = None) -> list[dict[str, Any]]:
    query = HotelMealPlan.find()
    if property_id:
        query = query.find(HotelMealPlan.property_id == property_id),
    meal_plans = await query.sort("-created_at").to_list()
    return [m.model_dump() for m in meal_plans]


async def get_meal_plan(db_name: str, *, meal_plan_id: str) -> dict[str, Any] | None:
    item = await HotelMealPlan.find_one(
        HotelMealPlan.id == meal_plan_id)
    return item.model_dump() if item else None


async def find_meal_plan_by_code(
    db_name: str,
    *,
    property_id: str,
    code: str) -> dict[str, Any] | None:
    item = await HotelMealPlan.find_one(
        HotelMealPlan.property_id == property_id,
        HotelMealPlan.code == code)
    return item.model_dump() if item else None


async def create_meal_plan(
    db_name: str,
    *,
    property_id: str,
    code: str,
    name: str,
    description: str | None,
    price_per_person_per_night_minor: int,
    currency: str,
    included_meals: list[str],
    is_active: bool) -> dict[str, Any]:
    model = HotelMealPlan(
        property_id=property_id,
        code=code,
        name=name,
        description=description,
        price_per_person_per_night_minor=price_per_person_per_night_minor,
        currency=currency,
        included_meals=included_meals,
        is_active=is_active)
    await model.insert()
    return model.model_dump()


async def list_guest_profiles(db_name: str) -> list[dict[str, Any]]:
    profiles = await HotelGuestProfile.find().sort("-created_at").to_list()
    return [p.model_dump() for p in profiles]


async def get_guest_profile(db_name: str, *, profile_id: str) -> dict[str, Any] | None:
    p = await HotelGuestProfile.find_one(
        HotelGuestProfile.id == profile_id)
    return p.model_dump() if p else None


async def find_guest_profile_by_email(db_name: str, *, email: str) -> dict[str, Any] | None:
    p = await HotelGuestProfile.find_one(
        HotelGuestProfile.email == email)
    return p.model_dump() if p else None


async def create_guest_profile(
    db_name: str,
    *,
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
    notes: str | None) -> dict[str, Any]:
    model = HotelGuestProfile(
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
        notes=notes)
    await model.insert()
    return model.model_dump()


async def list_rate_plans(
    db_name: str,
    *,
    property_id: str | None = None) -> list[dict[str, Any]]:
    query = HotelRatePlan.find()
    if property_id:
        query = query.find(HotelRatePlan.property_id == property_id),
    plans = await query.sort("-created_at").to_list()
    return [p.model_dump() for p in plans]


async def get_rate_plan(db_name: str, *, rate_plan_id: str) -> dict[str, Any] | None:
    p = await HotelRatePlan.find_one(
        HotelRatePlan.id == rate_plan_id)
    return p.model_dump() if p else None


async def create_rate_plan(
    db_name: str,
    *,
    property_id: str,
    room_type_id: str,
    label: str,
    currency: str,
    weekend_enabled: bool,
    weekend_rate_minor: int | None,
    seasonal_overrides: list[dict[str, Any]],
    is_active: bool) -> dict[str, Any]:
    model = HotelRatePlan(
        property_id=property_id,
        room_type_id=room_type_id,
        label=label,
        currency=currency,
        weekend_enabled=weekend_enabled,
        weekend_rate_minor=weekend_rate_minor,
        seasonal_overrides=seasonal_overrides,
        is_active=is_active)
    await model.insert()
    return model.model_dump()


async def list_availability_rules(
    db_name: str,
    *,
    property_id: str | None = None) -> list[dict[str, Any]]:
    query = HotelAvailabilityRule.find()
    if property_id:
        query = query.find(HotelAvailabilityRule.property_id == property_id),
    rules = await query.sort("-created_at").to_list()
    return [r.model_dump() for r in rules]


async def get_availability_rule(db_name: str, *, rule_id: str) -> dict[str, Any] | None:
    r = await HotelAvailabilityRule.find_one(
        HotelAvailabilityRule.id == rule_id)
    return r.model_dump() if r else None


async def create_availability_rule(
    db_name: str,
    *,
    property_id: str,
    room_type_id: str,
    total_units: int,
    minimum_stay_nights: int,
    maximum_stay_nights: int,
    blackout_dates: list[str],
    is_active: bool) -> dict[str, Any]:
    model = HotelAvailabilityRule(
        property_id=property_id,
        room_type_id=room_type_id,
        total_units=total_units,
        minimum_stay_nights=minimum_stay_nights,
        maximum_stay_nights=maximum_stay_nights,
        blackout_dates=blackout_dates,
        is_active=is_active)
    await model.insert()
    return model.model_dump()
