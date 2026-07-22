import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.auth.repo import RevokedTokenRepository
from app.core.config import settings

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self._job_id = "cleanup_tokens"

    async def init(self, app) -> None:

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

        self.scheduler.add_job(
            cleanup_revoked_tokens,
            "interval",
            hours=settings.jwt_scheduler_task_interval_hours,
            id=self._job_id,
            replace_existing=True,
        )

        self.scheduler.start()
        logger.info("Scheduler started")

    async def stop(self) -> None:
        if not self.scheduler.running:
            return

        self.scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
