from uuid import UUID

from app.account.repo import AccountRepository


class AccountService:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    async def get_user_accounts(self, user_id: UUID):
        return await self.account_repo.get_by_user_id(user_id)