from typing import TypeVar, Type, Any
from uuid import UUID

from app.account.models import Account
from app.core.models import BaseModel
from app.payment.models import Payment
from app.user.models import User

BaseType = TypeVar("BaseType", bound=BaseModel)

class EntityNotFoundError(Exception):

    def __init__(
        self,
        entity_type: Type[BaseType],
        entity_id: UUID | None = None,
        message: str | None = None,
    ):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.message = message if message else self._build_message()
        super().__init__(self.message)

    def _build_message(self) -> str:
        if self.entity_id is not None:
            return f"{self.entity_type} with id '{self.entity_id}' not found"
        return f"{self.entity_type} not found"

    def to_dict(self) -> dict:
        return {
            "error": "EntityNotFound",
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.__name__,
            "error_message": self.message,
        }

    def __str__(self) -> str:
        return self.message


class UserNotFoundError(EntityNotFoundError):
    def __init__(self, user_id: UUID):
        super().__init__(User, user_id)


class AccountNotFoundError(EntityNotFoundError):
    def __init__(self, node_id: UUID):
        super().__init__(Account, node_id)


class PaymentNotFoundError(EntityNotFoundError):
    def __init__(self, root_id: UUID):
        super().__init__(Payment, root_id)


class EntityAlreadyExistsError(Exception):
    def __init__(
        self,
        entity_type: Type[BaseType],
        fields: dict[str, Any] | None = None,
        message: str | None = None,
    ):
        self.entity_type = entity_type
        self.fields = fields
        self.message = message or self._build_message()

        super().__init__(self.message)

    def _build_message(self) -> str:
        if self.fields is not None:
            values = ", ".join(
                f"{field}={value}"
                for field, value in self.fields
            )

            return (
                # "User with email=jane@gmail.com, username=jane already exists"
                f"{self.entity_type.__name__} "
                f"with {values} already exists"
            )

        return f"{self.entity_type.__name__} already exists"

    def to_dict(self) -> dict:
        return {
            "error": "EntityAlreadyExists",
            "entity_type": self.entity_type.__name__,
            "fields": self.fields,
            "error_message": self.message,
        }

    def __str__(self) -> str:
        return self.message


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(User, fields)


class AccountAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Account, fields)


class PaymentAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Payment, fields)
