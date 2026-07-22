from typing import TypeVar, Type, Any
from uuid import UUID

from app.core.models import BaseModel


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
            return f"{self.entity_type.__name__} with id '{self.entity_id}' not found"
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






