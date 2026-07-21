from sanic import Blueprint
from sanic.response import JSONResponse

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.services import AuthService
from app.auth.types import CurrentUser

auth_bp = Blueprint("auth", url_prefix="/auth")


@auth_bp.post("/login")
async def login(request, auth_service: AuthService):
    data = LoginRequest.model_validate(request.json)
    token = await auth_service.login(data.email, data.password)

    return JSONResponse(TokenResponse(access_token=token).model_dump())


@auth_bp.post("/logout")
async def logout(
    request,
    _: CurrentUser,
    auth_service: AuthService,
):
    auth_header = request.headers.get(
        "Authorization"
    )

    token = auth_header.split(" ")[1]

    await auth_service.logout(
        token
    )

    return JSONResponse(
        {
            "status": "logged_out"
        },
    )