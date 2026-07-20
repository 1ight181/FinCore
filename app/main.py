from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Database


@asynccontextmanager
async def lifespan(
    application: FastAPI,
):
    database = None

    try:
        database = Database(
            config=settings.db_settings,
        )

        await database.health_check()

        application.state.database = database

        yield

    except Exception:
        raise

    finally:
        if database is not None:
            await database.dispose()


app = FastAPI(
    lifespan=lifespan,
)