from decimal import Decimal
from uuid import UUID

from app.account.models import Account
from app.account.repo import AccountRepository
from app.auth.security import hash_password
from app.core.exceptions import UserNotFoundError
from app.user.models import User
from app.user.repo import UserRepository
from app.user.schemas import AdminCreateUserRequest, UserUpdateRequest


class UserService:
    def __init__(self, user_repo: UserRepository, account_repo: AccountRepository):
        self.user_repo = user_repo
        self.account_repo = account_repo

    async def create_user(self, data: AdminCreateUserRequest) -> User:
        password_hash = hash_password(data.password)

        user = User(
            email=data.email,
            full_name=data.full_name,
            password_hash=password_hash,
        )

        await self.user_repo.create(user)

        account = Account(
            user_id=user.id,
            balance=Decimal("0")
        )
        await self.account_repo.create(account)

        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repo.get_by_id(user_id)

    async def get_by_id_with_accounts_and_payments(self, user_id: UUID) -> User | None:
        return await self.user_repo.get_with_accounts_and_payments(user_id)

    async def get_all_with_accounts_and_payments(self) -> list[User]:
        return await self.user_repo.get_all_with_accounts_and_payments()

    async def update_user(
            self,
            user_id: UUID,
            data: UserUpdateRequest,
    ):
        values = data.model_dump(
            exclude_unset=True
        )

        if "password" in values:
            values["password_hash"] = hash_password(
                values.pop("password")
            )

        user = await self.user_repo.update(
            user_id,
            values,
        )

        if not user:
            raise UserNotFoundError(user_id)

        return user

    async def delete_user(self, user_id: UUID, current_user: User):
        was_deleted = await self.user_repo.delete(user_id)

        if not was_deleted:
            raise UserNotFoundError(user_id)