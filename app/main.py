import logging

from sanic import Sanic
from sanic_ext import Extend

from app.auth.routers import auth_bp
from app.core.deps import setup_dependencies
from app.core.error_handlers import setup_error_handlers
from app.core.listeners import setup_listeners
from app.core.logger import setup_logger
from app.core.middleware import setup_middlewares
from app.user.routers import user_bp, admin_bp
from app.payment.routers import payment_bp

logger = logging.getLogger(__name__)

def create_app() -> Sanic:

    app = Sanic("FinCore")

    app.config.OAS_UI_DEFAULT = "swagger"
    ext: Extend = app.ext
    ext.openapi.add_security_scheme(
        "bearerAuth",
        "http",
        scheme="bearer",
        bearer_format="JWT",
    )

    setup_logger()

    app.blueprint(auth_bp)
    app.blueprint(user_bp)
    app.blueprint(payment_bp)
    app.blueprint(admin_bp)

    setup_middlewares(app)
    setup_listeners(app)
    setup_dependencies(app)
    setup_error_handlers(app)

    logger.info("Creating Sanic application")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True,
    )