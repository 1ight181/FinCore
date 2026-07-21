from typing import Any
from uuid import UUID

from app.core.exceptions import EntityNotFoundError, EntityAlreadyExistsError
from app.payment.models import Payment


class PaymentNotFoundError(EntityNotFoundError):
    def __init__(self, root_id: UUID):
        super().__init__(Payment, root_id)

class PaymentAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Payment, fields)

class InvalidPaymentSignatureError(Exception):
    pass