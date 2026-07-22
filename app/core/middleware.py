from sanic import Sanic


def setup_middlewares(app: Sanic):

    @app.middleware("request")
    async def create_session(request):
        request.ctx.session = (
            request.app.ctx.db.session_factory()
        )


    @app.middleware("response")
    async def close_session(request, _):
        await request.ctx.session.close()