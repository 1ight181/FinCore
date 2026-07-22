import logging

from sanic import Sanic

from app.core.config import settings
from app.core.database import Database
from app.core.scheduler import SchedulerService

logger = logging.getLogger(__name__)

def setup_listeners(app: Sanic):

    @app.before_server_start
    async def startup(app: Sanic):
        db = Database(settings.db)

        try:
            await db.health_check()
        except Exception as e:
            logger.exception(f"Failed to health check db: {e}")
            raise

        app.ctx.db = db
        app.ctx.scheduler = SchedulerService()
        await app.ctx.scheduler.init(app)

    @app.after_server_start
    async def after_startup(_: Sanic):
        logger.info("Sanic app started")

    @app.after_server_stop
    async def shutdown(app: Sanic):
        try:
            scheduler = getattr(app.ctx, "scheduler", None)
            if scheduler:
                await scheduler.stop()
        except Exception as e:
            logger.exception(f"Failed to stop scheduler: {e}")
            raise

        try:
            await app.ctx.db.dispose()
        except Exception as e:
            logger.exception(f"Failed to stop db: {e}")
            raise

        logger.info(f"Sanic app stopped")
