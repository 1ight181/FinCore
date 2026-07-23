from uuid import UUID

from sanic import Blueprint, Request, json
from sanic_ext import openapi

from app.payment.schemas import (
    WebhookPaymentRequest,
    WebhookSuccessResponse, WebhookPaymentRequestDocModel,
)
from app.payment.service import PaymentService
from app.core.transaction_manager import TransactionManager


payment_bp = Blueprint(
    "payment",
    url_prefix="/payment",
)


@payment_bp.post("/webhook")
@openapi.summary("Process payment webhook")
@openapi.description(
    """
    Processes incoming payment notification.

    The endpoint receives payment information from an external payment provider,
    updates account balance and returns transaction result.
    """
)
@openapi.body(
    {
        "application/json": WebhookPaymentRequestDocModel
    },
    description="Payment webhook payload"
)
@openapi.response(
    200,
    {
        "application/json": WebhookSuccessResponse
    },
    description="Payment successfully processed"
)
@openapi.response(
    400,
    description="Invalid webhook payload"
)
@openapi.response(
    409,
    description="Payment already processed"
)
async def payment_webhook(
    request: Request,
    service: PaymentService,
    transaction_manager: TransactionManager,
):
    data = WebhookPaymentRequest.model_validate(
        request.json
    )

    async with transaction_manager.begin():
        payment = await service.process_webhook(
            data
        )

    return json(
        WebhookSuccessResponse(
            transaction_id=payment.transaction_id,
            new_balance=payment.account.balance,
        )
        .model_dump(mode="json")
    )