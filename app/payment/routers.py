from uuid import UUID

from sanic import Blueprint, Request, json

from app.auth.types import CurrentUser
from app.payment.schemas import (
    WebhookPaymentRequest,
    WebhookSuccessResponse, PaymentResponse, PaymentListResponse,
)
from app.payment.service import PaymentService
from app.core.transaction_manager import TransactionManager


payment_bp = Blueprint(
    "payment",
    url_prefix="/payment",
)

@payment_bp.get("/<payment_id:uuid>")
async def get_payment(
    _,
    payment_id: UUID,
    service: PaymentService,
):

    payment = await service.get_by_id(
        payment_id
    )

    return json(
        PaymentResponse
        .model_validate(payment)
        .model_dump(mode="json")
    )

@payment_bp.get("/me")
async def get_my_payments(
    _,
    current_user: CurrentUser,
    service: PaymentService,
):

    payments = await service.get_user_payments(
        current_user.id
    )

    return json(
        PaymentListResponse(
            payments=[
                PaymentResponse.model_validate(p)
                for p in payments
            ]
        )
        .model_dump(mode="json")
    )


@payment_bp.post("/webhook")
async def payment_webhook(
    request: Request,
    service: PaymentService,
    transaction: TransactionManager,
):

    data = WebhookPaymentRequest.model_validate(
        request.json
    )


    async with transaction.begin():

        payment = await service.process_webhook(
            data
        )


    return json(
        WebhookSuccessResponse(
            transaction_id=payment.transaction_id,
            new_balance=payment.account.balance,
        )
        .model_dump(
            mode="json"
        )
    )