from sanic import Blueprint, json, empty
from sanic_ext import openapi

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.services import AuthService
from app.auth.types import CurrentUser


auth_bp = Blueprint(
    "auth",
    url_prefix="/auth",
)


@auth_bp.post("/login")
@openapi.summary("Login user")
@openapi.description(
    "Authenticate user by email and password and return JWT access token."
)
@openapi.body(
    {
        "application/json": LoginRequest
    },
)
@openapi.response(
    200,
    {
        "application/json": TokenResponse
    },
    description="Successful authentication"
)
@openapi.response(
    401,
    description="Invalid credentials"
)
async def login(
    request,
    auth_service: AuthService,
):
    data = LoginRequest.model_validate(request.json)

    token = await auth_service.login(
        data.email,
        data.password,
    )

    return json(
        TokenResponse(
            access_token=token
        ).model_dump(mode="json",)
    )


@auth_bp.post("/logout")
@openapi.summary("Logout user")
@openapi.description(
    "Invalidate current JWT token."
)
@openapi.secured("bearerAuth")
@openapi.response(
    200,
    description="Successfully logged out"
)
@openapi.response(
    401,
    description="Unauthorized"
)
async def logout(
    request,
    _: CurrentUser,
    auth_service: AuthService,
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return json(
            {
                "error": "unauthorized",
                "message": "Missing or invalid authorization header",
            },
            status=401,
        )

    token = auth_header.split(" ")[1]

    await auth_service.logout(token)

    return empty(
        status=200,
    )

