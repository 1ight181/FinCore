from uuid import UUID

from pydantic import Field
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.core.schemas import FromAttributes
from app.payment.schemas import PaymentResponse, PaymentResponseDocModel


class AccountResponse(FromAttributes):
    id: UUID
    user_id: UUID
    balance: Decimal = Field(..., ge=0, json_schema_extra={
            "example": "1000.10"
        })
    created_at: datetime

class AccountResponseDocModel(BaseModel):
    id: UUID
    user_id: UUID
    balance: Decimal = Field(..., ge=0, json_schema_extra={
        "example": "1000.10"
    })
    created_at: datetime

class AccountResponseWithPayments(AccountResponse):
    payments: list[PaymentResponse]

class AccountResponseWithPaymentsDocModel(AccountResponseDocModel):
    payments: list[PaymentResponseDocModel]

class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]

class AccountListResponseDocModel(BaseModel):
    accounts: list[AccountResponseDocModel]