from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.account.models import Account


class Payment(BaseModel, TimestampMixin):
    __tablename__ = "payments"


    transaction_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )


    account_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "accounts.id",
            ondelete="CASCADE"
        )
    )


    amount: Mapped[Decimal] = mapped_column(
        Numeric(
            12,
            2
        )
    )


    account: Mapped["Account"] = relationship(
        back_populates="payments",
    )
