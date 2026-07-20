from sanic.exceptions import Unauthorized

from app.auth.security import create_access_token, verify_password
from app.user.repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise Unauthorized("Invalid email or password")

        return create_access_token(subject=str(user.id))
