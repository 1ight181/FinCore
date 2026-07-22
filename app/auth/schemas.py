# login
from pydantic import Field, BaseModel, field_validator, validate_email


class LoginRequest(BaseModel):
    email: str = Field(
        description="User email",
        json_schema_extra={
            "format": "email",
            "example": "user@test.com"
        }
    )

    password: str = Field(
        min_length=1,
        json_schema_extra={
            "example": "password123"
        }
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        validate_email(value)
        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

