from datetime import datetime, UTC
from uuid import UUID

from jwt import InvalidTokenError
from sanic.exceptions import Unauthorized

from app.auth.models import RevokedToken
from app.auth.repo import RevokedTokenRepository
from app.auth.security import create_access_token, verify_password, decode_access_token
from app.user.repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository, revoked_token_repo: RevokedTokenRepository):
        self.user_repo = user_repo
        self.revoked_token_repo = revoked_token_repo

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise Unauthorized("Invalid email or password")

        return create_access_token(subject=str(user.id))

    async def logout(
            self,
            token: str,
    ) -> None:

        payload = decode_access_token(token)

        jti = payload.get("jti")
        user_id = payload.get("sub")
        expires_at = payload.get("exp")

        if not jti or not user_id or not expires_at:
            raise InvalidTokenError("Invalid jti")

        if await self.revoked_token_repo.is_revoked(str(jti)):
            return

        try:
            expires_at = int(str(expires_at))
        except ValueError:
            raise InvalidTokenError("Invalid token expires time")

        try:
            user_id = UUID(str(user_id))
        except ValueError:
            raise Unauthorized("Invalid user id")

        revoked_token = RevokedToken(
            token_jti=jti,
            user_id=user_id,
            expires_at=datetime.fromtimestamp(
                expires_at,
                UTC,
            ),
        )

        await self.revoked_token_repo.create(
            revoked_token
        )

    async def is_token_revoked(self, jti: str) -> bool:
        return await self.revoked_token_repo.is_revoked(jti)
