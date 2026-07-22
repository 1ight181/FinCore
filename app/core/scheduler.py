import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.auth.repo import RevokedTokenRepository
from app.core.config import settings

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)

def init_scheduler(app):

    async def cleanup_revoked_tokens():

        try:
            async with app.ctx.db.session_factory() as session:
                async with session.begin():
                    repo = RevokedTokenRepository(session)
                    await repo.cleanup_expired()

                    logger.info("Expired revoked tokens cleaned")

        except Exception as e:
            logger.exception(
                f"Failed to cleanup revoked tokens {e}"
            )


    scheduler.add_job(
        cleanup_revoked_tokens,
        "interval",
        hours=settings.jwt_scheduler_task_interval_hours,
        id="cleanup_tokens",
        replace_existing=True,
    )

    scheduler.start()