from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import (
    TravelDepartureModel,
    TravelItineraryDayModel,
    TravelLeadModel,
    TravelPackageModel,
)


def list_packages(db: Session, *, tenant_id: str) -> list[TravelPackageModel]:
    query = select(TravelPackageModel).where(TravelPackageModel.tenant_id == tenant_id)
    query = query.order_by(TravelPackageModel.created_at.desc())
    return list(db.scalars(query))


def get_package(db: Session, *, tenant_id: str, package_id: str) -> TravelPackageModel | None:
    query = select(TravelPackageModel).where(
        TravelPackageModel.tenant_id == tenant_id,
        TravelPackageModel.id == package_id,
    )
    return db.scalar(query)


def find_package_by_code(db: Session, *, tenant_id: str, code: str) -> TravelPackageModel | None:
    query = select(TravelPackageModel).where(
        TravelPackageModel.tenant_id == tenant_id,
        TravelPackageModel.code == code,
    )
    return db.scalar(query)


def find_package_by_slug(db: Session, *, tenant_id: str, slug: str) -> TravelPackageModel | None:
    query = select(TravelPackageModel).where(
        TravelPackageModel.tenant_id == tenant_id,
        TravelPackageModel.slug == slug,
    )
    return db.scalar(query)


def create_package(
    db: Session,
    *,
    tenant_id: str,
    code: str,
    slug: str,
    title: str,
    summary: str | None,
    origin_city: str,
    destination_city: str,
    destination_country: str,
    duration_days: int,
    base_price_minor: int,
    currency: str,
    status: str,
) -> TravelPackageModel:
    model = TravelPackageModel(
        tenant_id=tenant_id,
        code=code,
        slug=slug,
        title=title,
        summary=summary,
        origin_city=origin_city,
        destination_city=destination_city,
        destination_country=destination_country,
        duration_days=duration_days,
        base_price_minor=base_price_minor,
        currency=currency,
        status=status,
    )
    db.add(model)
    db.flush()
    return model


def list_itinerary_days(
    db: Session,
    *,
    tenant_id: str,
    package_ids: list[str],
) -> list[TravelItineraryDayModel]:
    if not package_ids:
        return []
    query = select(TravelItineraryDayModel).where(
        TravelItineraryDayModel.tenant_id == tenant_id,
        TravelItineraryDayModel.package_id.in_(package_ids),
    )
    query = query.order_by(TravelItineraryDayModel.package_id.asc(), TravelItineraryDayModel.day_number.asc())
    return list(db.scalars(query))


def create_itinerary_day(
    db: Session,
    *,
    tenant_id: str,
    package_id: str,
    day_number: int,
    title: str,
    summary: str,
    hotel_ref_id: str | None,
    activity_ref_ids: list[str],
    transfer_ref_ids: list[str],
) -> TravelItineraryDayModel:
    model = TravelItineraryDayModel(
        tenant_id=tenant_id,
        package_id=package_id,
        day_number=day_number,
        title=title,
        summary=summary,
        hotel_ref_id=hotel_ref_id,
        activity_ref_ids=activity_ref_ids,
        transfer_ref_ids=transfer_ref_ids,
    )
    db.add(model)
    db.flush()
    return model


def list_departures(
    db: Session,
    *,
    tenant_id: str,
    package_id: str | None = None,
    status: str | None = None,
) -> list[TravelDepartureModel]:
    query = select(TravelDepartureModel).where(TravelDepartureModel.tenant_id == tenant_id)
    if package_id:
        query = query.where(TravelDepartureModel.package_id == package_id)
    if status:
        query = query.where(TravelDepartureModel.status == status)
    query = query.order_by(TravelDepartureModel.departure_date.asc(), TravelDepartureModel.created_at.asc())
    return list(db.scalars(query))


def get_departure(db: Session, *, tenant_id: str, departure_id: str) -> TravelDepartureModel | None:
    query = select(TravelDepartureModel).where(
        TravelDepartureModel.tenant_id == tenant_id,
        TravelDepartureModel.id == departure_id,
    )
    return db.scalar(query)


def create_departure(
    db: Session,
    *,
    tenant_id: str,
    package_id: str,
    departure_date,
    return_date,
    seats_total: int,
    seats_available: int,
    price_override_minor: int | None,
    status: str,
) -> TravelDepartureModel:
    model = TravelDepartureModel(
        tenant_id=tenant_id,
        package_id=package_id,
        departure_date=departure_date,
        return_date=return_date,
        seats_total=seats_total,
        seats_available=seats_available,
        price_override_minor=price_override_minor,
        status=status,
    )
    db.add(model)
    db.flush()
    return model


def list_leads(
    db: Session,
    *,
    tenant_id: str,
    status: str | None = None,
    interested_package_id: str | None = None,
) -> list[TravelLeadModel]:
    query = select(TravelLeadModel).where(TravelLeadModel.tenant_id == tenant_id)
    if status:
        query = query.where(TravelLeadModel.status == status)
    if interested_package_id:
        query = query.where(TravelLeadModel.interested_package_id == interested_package_id)
    query = query.order_by(TravelLeadModel.created_at.desc())
    return list(db.scalars(query))


def get_lead(db: Session, *, tenant_id: str, lead_id: str) -> TravelLeadModel | None:
    query = select(TravelLeadModel).where(
        TravelLeadModel.tenant_id == tenant_id,
        TravelLeadModel.id == lead_id,
    )
    return db.scalar(query)


def create_lead(
    db: Session,
    *,
    tenant_id: str,
    source: str,
    interested_package_id: str | None,
    departure_id: str | None,
    customer_id: str | None,
    contact_name: str,
    contact_phone: str,
    travelers_count: int,
    desired_departure_date,
    budget_minor: int | None,
    currency: str,
    status: str,
    notes: str | None,
) -> TravelLeadModel:
    model = TravelLeadModel(
        tenant_id=tenant_id,
        source=source,
        interested_package_id=interested_package_id,
        departure_id=departure_id,
        customer_id=customer_id,
        contact_name=contact_name,
        contact_phone=contact_phone,
        travelers_count=travelers_count,
        desired_departure_date=desired_departure_date,
        budget_minor=budget_minor,
        currency=currency,
        status=status,
        notes=notes,
    )
    db.add(model)
    db.flush()
    return model
