from typing import Any
from uuid import UUID

from app.core.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from app.user.models import User


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(User, fields)


class UserNotFoundError(EntityNotFoundError):
    def __init__(self, user_id: UUID):
        super().__init__(User, user_id)

