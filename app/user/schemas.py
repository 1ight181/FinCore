from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, validate_email

from app.account.schemas import AccountResponseWithPayments, AccountResponseWithPaymentsDocModel
from app.core.schemas import FromAttributes
from app.user.role import UserRole


# common user
class UserBase(BaseModel):
    email: str
    full_name: str = Field(..., min_length=1, max_length=255)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        validate_email(value)
        return value


class UserCreateRequest(FromAttributes):
    email: str
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.USER

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        validate_email(value)
        return value

class UserCreateRequestDocModel(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.USER

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        validate_email(value)
        return value


class UserUpdateRequest(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is None:
            return value

        validate_email(value)
        return value


# admin
class UserResponse(UserBase):
    id: UUID
    role: UserRole
    created_at: datetime


class UserWithAccountsResponse(UserResponse):
    accounts: list[AccountResponseWithPayments]

class UserWithAccountsResponseDocModel(UserResponse):
    accounts: list[AccountResponseWithPaymentsDocModel]

class UserListResponse(BaseModel):
    users: list[UserWithAccountsResponse]
    total: int


class UserListResponseDocModel(BaseModel):
    users: list[UserWithAccountsResponseDocModel]
    total: int


class AdminUpdateUserRequest(UserUpdateRequest):
    role: UserRole | None = None