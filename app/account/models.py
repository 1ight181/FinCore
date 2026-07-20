from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.user.models import User
    from app.payment.models import Payment



class Account(BaseModel, TimestampMixin):
    __tablename__ = "accounts"


    __table_args__ = (
        CheckConstraint(
            "balance >= 0",
            name="positive_balance"
        ),
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )


    user: Mapped["User"] = relationship(
        back_populates="accounts",
    )


    balance: Mapped[Decimal] = mapped_column(
        Numeric(
            12,
            2
        ),
        default=0
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
    )
