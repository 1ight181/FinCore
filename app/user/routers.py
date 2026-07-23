from uuid import UUID

from sanic import Blueprint, json, empty, Forbidden
from sanic_ext import openapi

from app.account.services import AccountService
from app.auth.types import CurrentUser, AdminUser
from app.core.transaction_manager import TransactionManager
from app.payment.service import PaymentService
from app.user.exceptions import UserNotFoundError
from app.user.schemas import (
    UserResponse,
    UserListResponse,
    UserWithAccountsResponse, UserUpdateRequest, UserCreateRequest, UserCreateRequestDocModel, UserListResponseDocModel,
    UserWithAccountsResponseDocModel, UserResponseDocModel,
)
from app.account.schemas import AccountListResponse, AccountListResponseDocModel
from app.payment.schemas import PaymentListResponse, PaymentResponse, PaymentListResponseDocModel
from app.user.service import UserService


user_bp = Blueprint(
    "user",
    url_prefix="/users",
)


@user_bp.get("/me")
@openapi.summary("Get current user")
@openapi.description(
    "Returns information about the currently authenticated user."
)
@openapi.secured("bearerAuth")
@openapi.response(
    200,
    {
        "application/json": UserResponseDocModel
    },
    description="Current user information"
)
@openapi.response(
    401,
    description="Unauthorized"
)
async def get_me(
    _,
    current_user: CurrentUser,
):
    user_dump = UserResponse.model_validate(current_user.user).model_dump(mode="json")
    return json(
        user_dump
    )


@user_bp.get("/accounts")
@openapi.summary("Get user accounts")
@openapi.description(
    "Returns all accounts belonging to the currently authenticated user."
)
@openapi.secured("bearerAuth")
@openapi.response(
    200,
    {
        "application/json": AccountListResponseDocModel
    },
    description="List of user accounts"
)
@openapi.response(
    401,
    description="Unauthorized"
)
async def get_my_accounts(
    _,
    current_user: CurrentUser,
    account_service: AccountService,
):
    accounts = await account_service.get_user_accounts(
        current_user.user.id
    )

    return json(
        AccountListResponse(
            accounts=accounts
        ).model_dump(mode="json")
    )


@user_bp.get("/payments")
@openapi.summary("Get user payments")
@openapi.description(
    "Returns payment history of the currently authenticated user."
)
@openapi.secured("bearerAuth")
@openapi.response(
    200,
    {
        "application/json": PaymentListResponseDocModel
    },
    description="List of user payments"
)
@openapi.response(
    401,
    description="Unauthorized"
)
async def get_my_payments(
    _,
    current_user: CurrentUser,
    payment_service: PaymentService,
):
    payments = await payment_service.get_user_payments(
        current_user.user.id
    )

    payment_list_response = PaymentListResponse(
        payments=[
            PaymentResponse.model_validate(payment)
            for payment in payments
        ]
    )

    return json(
        payment_list_response.model_dump(
            mode="json",
        )
    )


admin_bp = Blueprint(
    "admin",
    url_prefix="/admin",
)


@admin_bp.post("/users")
@openapi.summary("Create user")
@openapi.description(
    "Creates a new user. Requires administrator privileges."
)
@openapi.secured("bearerAuth")
@openapi.body(
    {
        "application/json": UserCreateRequestDocModel
    }
)
@openapi.response(
    201,
    {
        "application/json": UserResponseDocModel
    },
    description="User successfully created"
)
@openapi.response(
    401,
    description="Unauthorized"
)
@openapi.response(
    403,
    description="Forbidden. Administrator privileges required."
)
async def create_user(
    request,
    user_service: UserService,
    __: AdminUser,
    transaction_manager: TransactionManager,
):
    data = UserCreateRequest.model_validate(
        request.json
    )
    
    async with transaction_manager.begin():
        user = await user_service.create_user(
            data,
        )

    return json(
        UserResponse.model_validate(user).model_dump(
            mode="json"
        ),
        status=201,
    )


@admin_bp.get("/users")
@openapi.summary("Get users")
@openapi.description(
    "Returns list of all users with accounts and payments. Requires administrator privileges."
)
@openapi.secured("bearerAuth")
@openapi.response(
    200,
    {
        "application/json": UserListResponseDocModel
    },
    description="List of users"
)
@openapi.response(
    401,
    description="Unauthorized"
)
@openapi.response(
    403,
    description="Forbidden. Administrator privileges required."
)
async def get_users(
    _,
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

    return json(
        user_list_response.model_dump(mode="json")
    )


@admin_bp.get("/users/<user_id:uuid>")
@openapi.summary("Get user by id")
@openapi.description(
    "Returns detailed user information including accounts and payments."
)
@openapi.secured("bearerAuth")
@openapi.response(
    200,
    {
        "application/json": UserWithAccountsResponseDocModel
    },
    description="User information"
)
@openapi.response(
    401,
    description="Unauthorized"
)
@openapi.response(
    403,
    description="Forbidden. Administrator privileges required."
)
async def get_user(
    _,
    user_id: UUID,
    user_service: UserService,
    ___: AdminUser,
):
    user = await user_service.get_by_id_with_accounts_and_payments(user_id)
    if not user:
        raise UserNotFoundError(user_id)

    return json(
        UserWithAccountsResponse
        .model_validate(user)
        .model_dump(mode="json")
    )


@admin_bp.put("/users/<user_id:uuid>")
@openapi.summary("Update user")
@openapi.description(
    "Updates user information. Requires administrator privileges."
)
@openapi.secured("bearerAuth")
@openapi.body(
    {
        "application/json": UserUpdateRequest
    }
)
@openapi.response(
    200,
    {
        "application/json": UserResponseDocModel
    },
    description="User successfully updated"
)
@openapi.response(
    401,
    description="Unauthorized"
)
@openapi.response(
    403,
    description="Forbidden. Administrator privileges required."
)
async def update_user(
    request,
    user_id: UUID,
    user_service: UserService,
    _: AdminUser,
):
    raw_data = request.json
    data = UserUpdateRequest.model_validate(
        raw_data,
    )

    user = await user_service.update_user(
        user_id,
        data,
    )

    return json(
        UserResponse
        .model_validate(user)
        .model_dump(mode="json")
    )


@admin_bp.delete("/users/<user_id:uuid>")
@openapi.summary("Delete user")
@openapi.description(
    "Deletes user by id. Requires administrator privileges."
)
@openapi.secured("bearerAuth")
@openapi.response(
    204,
    description="User successfully deleted"
)
@openapi.response(
    401,
    description="Unauthorized"
)
@openapi.response(
    403,
    description="Forbidden. Administrator privileges required."
)
async def delete_user(
    _,
    user_id: UUID,
    user_service: UserService,
    current_user: AdminUser,
):
    await user_service.delete_user(
        user_id,
    )

    return empty(
        status=204,
    )