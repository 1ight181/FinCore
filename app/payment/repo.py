from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import Account
from app.core.repo import BaseRepository
from app.payment.models import Payment


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Payment)

    async def get_by_transaction_id(self, transaction_id: str) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(Payment.transaction_id == transaction_id)
        )

        return result.scalar_one_or_none()

    async def get_user_payments(self, user_id: UUID):
        result = await self.session.execute(
            select(Payment)
            .join(Account)
            .where(Account.user_id == user_id)
            .order_by(Payment.created_at.desc())
        )

        return result.scalars().all()