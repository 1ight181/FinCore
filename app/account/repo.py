from uuid import UUID
from decimal import Decimal
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import Account
from app.core.constraint_registry import ConstraintRegistry
from app.core.repo import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: AsyncSession, constraint_registry: ConstraintRegistry):
        super().__init__(session, Account, constraint_registry)

    async def get_by_user_id(self, user_id: UUID) -> list[Account]:
        result = await self.session.execute(
            select(Account).where(Account.user_id == user_id)
        )

        return list(result.scalars().all())

    async def add_balance(self, account_id: UUID, amount: Decimal):
        stmt = (
            update(Account)
            .where(Account.id == account_id)
            .values(balance=Account.balance + amount)
        )

        await self.session.execute(stmt)
        await self.session.flush()
