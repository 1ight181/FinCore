from sanic import Request
from sanic.exceptions import Unauthorized, Forbidden

from app.auth.types import CurrentUser, AdminUser
from app.user.models import User
from app.auth.security import decode_access_token
from app.user.role import UserRole
from app.user.service import UserService


async def get_current_user(
    request: Request,
    service: UserService,
) -> User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Unauthorized("Missing or invalid authorization header")

    token = auth_header.split(" ")[1]
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise Unauthorized("Invalid token payload")

    try:
        user_id = int(str(user_id))
    except ValueError:
        raise Unauthorized("Invalid token")

    user = await service.get_by_id(user_id)

    if not user:
        raise Unauthorized("User not found")

    return user


async def require_admin(
    current_user: CurrentUser,
) -> AdminUser:

    if current_user.role != UserRole.ADMIN:
        raise Forbidden()

    return AdminUser(current_user)