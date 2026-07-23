from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.account.models import Account
from app.core.constraint_registry import ConstraintRegistry
from app.core.repo import BaseRepository
from app.user.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession, constraint_registry: ConstraintRegistry):
        super().__init__(session, User, constraint_registry)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_with_accounts_and_payments(
            self,
            user_id: UUID,
    ) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(joinedload(User.accounts).joinedload(Account.payments))
            .where(User.id == user_id)
        )

        return result.unique().scalar_one_or_none()

    async def get_all_with_accounts_and_payments(self) -> list[User]:
        result = await self.session.execute(
            select(User)
            .options(joinedload(User.accounts).joinedload(Account.payments))
            .order_by(User.id)
        )

        return list(result.unique().scalars().all())
