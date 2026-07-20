from sanic import Blueprint
from sanic.response import JSONResponse

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.services import AuthService

auth_bp = Blueprint("auth", url_prefix="/auth")


@auth_bp.post("/login")
async def login(request, auth_service: AuthService):
    data = LoginRequest.model_validate(request.json)
    token = await auth_service.login(data.email, data.password)
    return JSONResponse(TokenResponse(access_token=token).model_dump())

