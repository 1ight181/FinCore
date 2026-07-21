from typing import Any
from uuid import UUID

from app.account.models import Account
from app.core.exceptions import EntityNotFoundError, EntityAlreadyExistsError


class AccountNotFoundError(EntityNotFoundError):
    def __init__(self, node_id: UUID):
        super().__init__(Account, node_id)


class AccountAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Account, fields)
