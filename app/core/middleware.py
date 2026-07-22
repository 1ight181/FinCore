import logging

from sanic import Sanic


logger = logging.getLogger(__name__)

def setup_middlewares(app: Sanic):

    @app.middleware("response")
    async def close_session(request, response):

        logger.debug(f"Create session for {request}")
        session = getattr(request.ctx, "session", None)

        if session:
            try:
                if session.in_transaction():
                    if response.status < 400:
                        await session.commit()
                    else:
                        await session.rollback()

            finally:
                await session.close()

        return response