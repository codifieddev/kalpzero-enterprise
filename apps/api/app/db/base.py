from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def generate_uuid() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
