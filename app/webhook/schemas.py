from decimal import Decimal

from pydantic import Field, ConfigDict

from app.core.models import BaseModel


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