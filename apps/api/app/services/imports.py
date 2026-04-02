from sqlalchemy.orm import Session

from app.repositories import imports as import_repository
from app.repositories import platform as platform_repository
from app.services.errors import NotFoundError
from app.services.platform import serialize_audit_event, serialize_outbox_event


def serialize_import_source(source) -> dict[str, object]:
    return {
        "id": source.id,
        "tenant_id": source.tenant_id,
        "name": source.name,
        "source_type": source.source_type,
        "connection_profile_key": source.connection_profile_key,
        "vertical_pack": source.vertical_pack,
        "config": source.config_json,
        "created_at": source.created_at.isoformat(),
    }


def serialize_import_job(job) -> dict[str, object]:
    return {
        "id": job.id,
        "tenant_id": job.tenant_id,
        "source_id": job.source_id,
        "requested_by_user_id": job.requested_by_user_id,
        "mode": job.mode,
        "status": job.status,
        "report": job.report_json,
        "created_at": job.created_at.isoformat(),
        "finished_at": job.finished_at,
    }


def create_import_source(
    db: Session,
    *,
    tenant_slug: str,
    actor_user_id: str,
    name: str,
    source_type: str,
    connection_profile_key: str,
    vertical_pack: str,
    config_json: dict[str, object],
) -> dict[str, object]:
    tenant = platform_repository.get_tenant_by_slug(db, tenant_slug)
    if tenant is None:
        raise NotFoundError(f"Tenant '{tenant_slug}' was not found.")

    source = import_repository.create_import_source(
        db,
        tenant_id=tenant.id,
        name=name,
        source_type=source_type,
        connection_profile_key=connection_profile_key,
        vertical_pack=vertical_pack,
        config_json=config_json,
    )
    platform_repository.create_audit_event(
        db,
        tenant_id=tenant.id,
        actor_user_id=actor_user_id,
        action="imports.source.created",
        subject_type="import_source",
        subject_id=source.id,
        metadata_json={"source_type": source.source_type, "vertical_pack": source.vertical_pack},
    )
    db.commit()
    return serialize_import_source(source)


def list_import_sources(db: Session, *, tenant_slug: str) -> list[dict[str, object]]:
    tenant = platform_repository.get_tenant_by_slug(db, tenant_slug)
    if tenant is None:
        raise NotFoundError(f"Tenant '{tenant_slug}' was not found.")

    return [serialize_import_source(item) for item in import_repository.list_import_sources(db, tenant_id=tenant.id)]


def create_import_job(
    db: Session,
    *,
    tenant_slug: str,
    actor_user_id: str,
    source_id: str,
    mode: str,
) -> dict[str, object]:
    tenant = platform_repository.get_tenant_by_slug(db, tenant_slug)
    if tenant is None:
        raise NotFoundError(f"Tenant '{tenant_slug}' was not found.")

    source = import_repository.get_import_source(db, source_id=source_id, tenant_id=tenant.id)
    if source is None:
        raise NotFoundError(f"Import source '{source_id}' was not found.")

    report_json = {
        "stage": "queued",
        "summary": "Job accepted for canonical validation and worker processing.",
        "supports_dry_run": True,
    }
    job = import_repository.create_import_job(
        db,
        tenant_id=tenant.id,
        source_id=source.id,
        requested_by_user_id=actor_user_id,
        mode=mode,
        status="queued",
        report_json=report_json,
    )
    audit_event = platform_repository.create_audit_event(
        db,
        tenant_id=tenant.id,
        actor_user_id=actor_user_id,
        action="imports.job.created",
        subject_type="import_job",
        subject_id=job.id,
        metadata_json={"source_id": source.id, "mode": mode},
    )
    outbox_event = platform_repository.enqueue_outbox_event(
        db,
        tenant_id=tenant.id,
        aggregate_id=job.id,
        event_name="import.job.queued",
        payload_json={
            "tenant_slug": tenant.slug,
            "source_id": source.id,
            "mode": mode,
            "source_type": source.source_type,
        },
    )
    db.commit()
    return {
        "job": serialize_import_job(job),
        "audit_event": serialize_audit_event(audit_event),
        "outbox_event": serialize_outbox_event(outbox_event),
    }


def list_import_jobs(db: Session, *, tenant_slug: str) -> list[dict[str, object]]:
    tenant = platform_repository.get_tenant_by_slug(db, tenant_slug)
    if tenant is None:
        raise NotFoundError(f"Tenant '{tenant_slug}' was not found.")

    return [serialize_import_job(item) for item in import_repository.list_import_jobs(db, tenant_id=tenant.id)]
