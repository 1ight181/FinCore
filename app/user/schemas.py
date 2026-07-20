from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from app.account.schemas import AccountResponse
from app.user.role import UserRole


# common user
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreateRequest(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)


# admin
class UserResponse(UserBase):
    id: UUID
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithAccountsResponse(UserResponse):
    accounts: list[AccountResponse]


class UserListResponse(BaseModel):
    users: list[UserWithAccountsResponse]
    total: int


class AdminCreateUserRequest(UserCreateRequest):
    role: UserRole = UserRole.USER


class AdminUpdateUserRequest(UserUpdateRequest):
    role: UserRole | None = None