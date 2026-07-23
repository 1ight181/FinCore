import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class TransactionManager:

    def __init__(self, session: AsyncSession):
        self.session = session

    @asynccontextmanager
    async def begin(self):
        if self.session.in_transaction():
            try:
                yield
            except Exception:
                logger.exception(
                    "Transaction failed, rollback"
                )
                await self.session.rollback()
                raise
            return

        async with self.session.begin():
            yield
