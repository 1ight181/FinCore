from typing import TypeVar, Generic
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constraint_registry import ConstraintRegistry
from app.core.exceptions import EntityAlreadyExistsError
from app.core.models import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType], constraint_registry: ConstraintRegistry | None = None):
        self.session = session
        self.model = model
        self.constraint_registry = constraint_registry

    async def get_by_id(self, id: UUID):
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def create(self, new: ModelType) -> ModelType:
        self.session.add(new)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            constraint_name = getattr(exc.orig, "constraint_name", None)
            if not self.constraint_registry:
                raise EntityAlreadyExistsError(type(new))

            fields = self.constraint_registry.get_fields_for_unique_constraint(constraint_name)
            fields_with_values = {field: getattr(new, field) for field in fields}

            raise EntityAlreadyExistsError(type(new), fields_with_values)

        return new


    async def update(self, id: UUID, values: dict) -> ModelType | None:
        old = await self.get_by_id(id)
        if not old:
            return None

        for field, value in values.items():
            setattr(old, field, value)

        await self.session.flush()

        return old

    async def delete(self, id: UUID) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            return False

        await self.session.delete(instance)
        await self.session.flush()

        return True
