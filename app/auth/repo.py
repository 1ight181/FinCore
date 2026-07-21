from datetime import datetime, UTC
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RevokedToken
from app.core.repo import BaseRepository


class RevokedTokenRepository(BaseRepository[RevokedToken]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(session, RevokedToken)

    async def is_revoked(self, jti: str) -> bool:
        result = await self.session.execute(
            select(RevokedToken).where(RevokedToken.token_jti == jti)
        )

        return result.scalar_one_or_none() is not None

    async def cleanup_expired(self):
        await self.session.execute(
            delete(RevokedToken).where(RevokedToken.expires_at < datetime.now(UTC))
        )

        await self.session.flush()