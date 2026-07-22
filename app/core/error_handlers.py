import logging

from jwt import InvalidTokenError
from pydantic import ValidationError
from sanic import Sanic, json, Forbidden, Unauthorized
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import EntityNotFoundError, EntityAlreadyExistsError
from app.payment.exceptions import PaymentAlreadyExistsError, InvalidPaymentSignatureError

logger = logging.getLogger(__name__)

def setup_error_handlers(app: Sanic) -> None:
    @app.exception(Exception)
    async def handle_unknown_error(_, exception):
        logger.exception(
            "Unhandled exception",
            exc_info=exception,
        )

        return json(
            {
                "error": "internal_server_error",
            },
            status=500,
        )

    @app.exception(NotFound)
    async def handle_not_found_error(_, exception):
        logger.error(
            "Not found error",
            exc_info=exception,
        )

        return json(
            {"message": "Not Found"},
            status=404,
        )

    @app.exception(EntityNotFoundError)
    async def entity_not_found(
        _,
        exception,
    ):
        return json(
            {
                "error": "not_found",
                "message": str(exception)
            },
            status=404,
        )

    @app.exception(EntityAlreadyExistsError)
    async def entity_already_exists(
            _,
            exception,
    ):
        return json(
            {
                "error": "already_exists",
                "message": str(exception)
            },
            status=409,
        )

    @app.exception(PaymentAlreadyExistsError)
    async def handle_payment_exists(_, __):
        return json(
            {
                "error": "payment_exists",
                "message": "Payment already processed",
            },
            status=409,
        )

    @app.exception(IntegrityError)
    async def handle_integrity_error(
            _,
            exception,
    ):
        logger.exception(
            "Unhandled database integrity error",
            exc_info=exception,
        )

        return json(
            {
                "error": "db_error",
            },
            status=500,
        )

    @app.exception(InvalidPaymentSignatureError)
    async def handle_invalid_payment_signature():
        return json(
            {
                "error": "invalid_payment_signature",
                "message": "Invalid payment signature",
            },
            status=400,
        )

    @app.exception(ValidationError)
    async def handle_validation_error(
            _,
            exception: ValidationError,
    ):
        return json(
            {
                "error": "validation_error",
                "details": exception.errors(),
            },
            status=422,
        )

    @app.exception(InvalidTokenError)
    async def handle_invalid_token_error(
            _,
            exception: InvalidTokenError,
    ):
        return json(
            {
                "error": "invalid_token_error",
                "details": str(exception)
            },
            status=400,
        )

    @app.exception(Unauthorized)
    async def handle_unauthorized(
            _,
            exception: Unauthorized,
    ):
        return json(
            {
                "error": "unauthorized",
                "message": str(exception),
            },
            status=401,
        )

    @app.exception(Forbidden)
    async def handle_forbidden(
            _,
            exception: Forbidden,
    ):
        return json(
            {
                "error": "forbidden",
                "message": str(exception),
            },
            status=403,
        )

