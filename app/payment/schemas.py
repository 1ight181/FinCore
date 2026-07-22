from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.core.schemas import FromAttributes


class PaymentResponse(FromAttributes):
    id: UUID
    transaction_id: str
    account_id: UUID
    amount: Decimal = Field(..., gt=0, json_schema_extra={
        "example": "1000.10"
    })
    created_at: datetime

class PaymentResponseDocModel(BaseModel):
    id: UUID
    transaction_id: str
    account_id: UUID
    amount: Decimal = Field(..., gt=0, json_schema_extra={
        "example": "1000.10"
    })
    created_at: datetime

class PaymentListResponse(BaseModel):
    payments: list[PaymentResponse]


class PaymentListResponseDocModel(BaseModel):
    payments: list[PaymentResponseDocModel]


class WebhookPaymentRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=255)
    user_id: UUID
    account_id: UUID
    amount: Decimal = Field(..., gt=0, json_schema_extra={
        "example": "1000.10"
    })
    signature: str = Field(..., min_length=64, max_length=64)

    model_config = ConfigDict(extra="forbid")

class WebhookPaymentRequestDocModel(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=255)
    user_id: UUID
    account_id: UUID
    amount: Decimal = Field(..., gt=0, json_schema_extra={
        "example": "1000.10"
    })
    signature: str = Field(..., min_length=64, max_length=64)


class WebhookSuccessResponse(BaseModel):
    status: str = "success"
    transaction_id: str
    new_balance: Decimal = Field(..., gt=0, json_schema_extra={
        "example": "1000.10"
    })