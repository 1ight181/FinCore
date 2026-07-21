from uuid import UUID

from sanic import Blueprint
from sanic.response import JSONResponse

from app.account.services import AccountService
from app.auth.types import CurrentUser, AdminUser
from app.payment.service import PaymentService
from app.user.schemas import UserResponse, AdminCreateUserRequest, UserListResponse, UserWithAccountsResponse, \
    UserUpdateRequest
from app.account.schemas import  AccountListResponse
from app.payment.schemas import PaymentListResponse, PaymentResponse

from app.user.models import User
from app.user.service import UserService

# common user
user_bp = Blueprint("user", url_prefix="/users")


@user_bp.get("/me")
async def get_me(_, current_user: CurrentUser):
    return JSONResponse(UserResponse.model_validate(current_user).model_dump())


@user_bp.get("/accounts")
async def get_my_accounts(
    _,
    current_user: CurrentUser,
    account_service: AccountService
):
    accounts = await account_service.get_user_accounts(current_user.id)

    return JSONResponse(AccountListResponse(accounts=accounts).model_dump())


@user_bp.get("/payments")
async def get_my_payments(
    _,
    current_user: CurrentUser,
    payment_service: PaymentService
):
    payments = await payment_service.get_user_payments(current_user.id)

    payment_list_response = PaymentListResponse(
        payments=[
            PaymentResponse.model_validate(payment)
            for payment in payments
        ]
    )

    return JSONResponse(payment_list_response.model_dump())


# admin user
admin_bp = Blueprint("admin", url_prefix="/admin")


@admin_bp.post("/users")
async def create_user(
    request,
    _: User,
    user_service: UserService,
    __: AdminUser,
):
    data = AdminCreateUserRequest.model_validate(request.json)
    user = await user_service.create_user(data)

    return JSONResponse(UserResponse.model_validate(user).model_dump(), status=201)


@admin_bp.get("/users")
async def get_users(
    _,
    __: User,
    user_service: UserService,
    ___: AdminUser,
):
    users = await user_service.get_all_with_accounts_and_payments()
    user_list_response = UserListResponse(
        users=[
            UserWithAccountsResponse.model_validate(user)
            for user in users
        ],
        total=len(users),
    )

    return JSONResponse(user_list_response.model_dump())


@admin_bp.get("/users/<user_id:uuid>")
async def get_user(
    _,
    user_id: UUID,
    __: User,
    user_service: UserService,
    ___: AdminUser,
):
    user = await user_service.get_by_id(user_id)
    return JSONResponse(UserWithAccountsResponse.model_validate(user).model_dump())


@admin_bp.put("/users/<user_id:uuid>")
async def update_user(
    request,
    user_id: UUID,
    user_service: UserService,
    _: AdminUser,
):
    data = UserUpdateRequest.model_validate(request.json)
    user = await user_service.update_user(user_id, data)

    return JSONResponse(UserResponse.model_validate(user).model_dump())


@admin_bp.delete("/users/<user_id:uuid>")
async def delete_user(
    _,
    user_id: UUID,
    current_user: User,
    user_service: UserService,
    __: AdminUser,
):
    await user_service.delete_user(user_id, current_user)

    return JSONResponse({"status": "deleted"}, status=204)