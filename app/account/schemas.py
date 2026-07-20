from pydantic import Field
from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict

from app.core.models import BaseModel


class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: Decimal = Field(..., ge=0)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]