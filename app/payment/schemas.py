from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict

from app.core.models import BaseModel


class PaymentResponse(BaseModel):
    id: int
    transaction_id: str
    account_id: int
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    payments: list[PaymentResponse]