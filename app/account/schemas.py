from uuid import UUID

from pydantic import Field
from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, BaseModel

from app.payment.schemas import PaymentResponse


class AccountResponse(BaseModel):
    id: UUID
    user_id: UUID
    balance: Decimal = Field(..., ge=0)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountResponseWithPayments(AccountResponse):
    payments: list[PaymentResponse]

class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]