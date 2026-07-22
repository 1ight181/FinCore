from datetime import datetime
from uuid import UUID

from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from app.core.models import BaseModel


class RevokedToken(BaseModel):
    __tablename__ = "revoked_tokens"

    __table_args__ = (
        UniqueConstraint(
            "token_jti",
            name="uq_revoked_tokens_token_jti"
        ),
    )

    token_jti: Mapped[str] = mapped_column(
        String(255),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )