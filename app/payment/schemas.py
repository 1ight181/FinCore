from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import ConfigDict, BaseModel


class PaymentResponse(BaseModel):
    id: UUID
    transaction_id: str
    account_id: int
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    payments: list[PaymentResponse]



class WebhookPaymentRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=255)
    user_id: int
    account_id: int
    amount: Decimal = Field(..., gt=0)
    signature: str = Field(..., min_length=64, max_length=64)

    model_config = ConfigDict(extra="forbid")


class WebhookSuccessResponse(BaseModel):
    status: str = "success"
    transaction_id: str
    new_balance: Decimal