import logging
from app.core.config import settings


def setup_logger():
    logger_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=logger_level,
        format=(
            "%(asctime)s "
            "[%(levelname)s] "
            "%(name)s: "
            "%(message)s"
        ),
    )