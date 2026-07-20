from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession


from app.core.config import DatabaseConfig

class Database:
    def __init__(
        self,
        config: DatabaseConfig,
    ):
        self._engine: AsyncEngine = create_async_engine(
            config.get_postgres_dsn(),
            pool_pre_ping=True,
        )

        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )


    @property
    def session_factory(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        return self._session_factory


    async def health_check(self) -> None:
        async with self.session_factory() as session:
           await session.execute(text("SELECT 1"))


    async def dispose(self) -> None:
        await self._engine.dispose()