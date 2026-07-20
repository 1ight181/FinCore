from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.account.models import Account


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel, TimestampMixin):
    __tablename__ = "users"


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )


    password_hash: Mapped[str] = mapped_column(
        String(255)
    )


    full_name: Mapped[str] = mapped_column(
        String(255)
    )


    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        name = "user_role"
    )


    accounts: Mapped[list["Account"]] = relationship(
        back_populates="user",
        cascade = "all, delete-orphan"
    )