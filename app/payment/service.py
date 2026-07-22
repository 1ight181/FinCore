import hashlib
import hmac

from decimal import Decimal
from uuid import UUID

from app.account.models import Account
from app.account.repo import AccountRepository
from app.core.config import settings
from app.core.exceptions import EntityNotFoundError
from app.payment.exceptions import (
    InvalidPaymentSignatureError,
    PaymentAlreadyExistsError,
)
from app.payment.models import Payment
from app.payment.repo import PaymentRepository
from app.payment.schemas import WebhookPaymentRequest
from app.user.models import User
from app.user.repo import UserRepository


class PaymentService:

    def __init__(
        self,
        payment_repo: PaymentRepository,
        account_repo: AccountRepository,
        user_repo: UserRepository,
    ):
        self.payment_repo = payment_repo
        self.account_repo = account_repo
        self.user_repo = user_repo

    async def get_by_id(
            self,
            payment_id: UUID,
    ) -> Payment:

        payment = await self.payment_repo.get_by_id(
            payment_id
        )

        if not payment:
            raise EntityNotFoundError(
                Payment,
                payment_id,
            )

        return payment

    async def get_user_payments(
            self,
            user_id: UUID,
    ) -> list[Payment]:

        return await self.payment_repo.get_user_payments(
            user_id
        )

    async def process_webhook(
        self,
        data: WebhookPaymentRequest,
    ) -> Payment:

        self._verify_signature(data)

        existing = await self.payment_repo.get_by_transaction_id(
            data.transaction_id
        )

        if existing:
            raise PaymentAlreadyExistsError(
                {
                    "transaction_id": data.transaction_id
                }
            )

        user = await self.user_repo.get_by_id(data.user_id)
        if not user:
            raise EntityNotFoundError(User, data.user_id)

        account = await self.account_repo.get_by_id(
            data.account_id
        )

        if account:
            if account.user_id != data.user_id:
                raise EntityNotFoundError(Account, data.account_id)
        else:
            account = Account(
                id=data.account_id,
                user_id=data.user_id,
                balance=Decimal("0"),
            )

            await self.account_repo.create(account)


        payment = Payment(
            transaction_id=data.transaction_id,
            account_id=account.id,
            amount=data.amount,
        )


        await self.payment_repo.create(payment)


        account.balance += data.amount


        return payment



    @staticmethod
    def _verify_signature(
            data: WebhookPaymentRequest,
    ):

        raw = (
            f"{data.account_id}"
            f"{data.amount}"
            f"{data.transaction_id}"
            f"{data.user_id}"
            f"{settings.webhook_secret_key}"
        )


        signature = hashlib.sha256(
            raw.encode()
        ).hexdigest()


        if not hmac.compare_digest(
            signature,
            data.signature,
        ):
            raise InvalidPaymentSignatureError()