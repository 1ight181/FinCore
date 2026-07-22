import logging

from sanic import Sanic

from app.auth.routers import auth_bp
from app.core.deps import setup_dependencies
from app.core.listeners import setup_listeners
from app.core.logger import setup_logger
from app.core.middleware import setup_middlewares
from app.core.scheduler import init_scheduler
from app.user.routers import user_bp


logger = logging.getLogger(__name__)

def create_app() -> Sanic:
    app = Sanic("FinCore")

    setup_logger()

    app.blueprint(auth_bp)
    app.blueprint(user_bp)

    setup_middlewares(app)
    setup_listeners(app)
    setup_dependencies(app)

    # to expire revoked jwt tokens
    init_scheduler(app)

    return app


