from datetime import datetime
from uuid import uuid4, UUID as MappedUUID

from sqlalchemy import func, UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[MappedUUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )