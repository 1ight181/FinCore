from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True


    id: Mapped[int] = mapped_column(
        primary_key=True
    )