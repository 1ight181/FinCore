from sanic import Request
from sanic.exceptions import Unauthorized
from app.user.models import User
from app.user.services import UserService
from app.auth.security import decode_access_token


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
