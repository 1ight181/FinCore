from sqlalchemy import UniqueConstraint, Table

from app.core.models import BaseModel


class ConstraintRegistry:
    unique_constraints: dict[str, list[str]]

    def __init__(self, models: list[type[BaseModel]]):

        for model in models:
            self.unique_constraints.update(self._build_unique_constraint_map(model))


    @staticmethod
    def _build_unique_constraint_map(model: type[BaseModel]) -> dict[str, list[str]]:
        table = model.__table__
        assert isinstance(table, Table)

        result = {}

        for constraint in table.constraints:
            if (
                    isinstance(constraint, UniqueConstraint)
                    and constraint.name
            ):
                result[constraint.name] = [
                    column.name
                    for column in constraint.columns
                ]

        return result

    def get_fields_for_unique_constraint(self, constraint_name) -> list[str]:
        return self.unique_constraints[constraint_name]