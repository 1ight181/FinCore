from sanic import Sanic
from sanic_ext import Extend
from sqlalchemy.ext.asyncio import AsyncSession
from sanic.request import Request

from app.account.models import Account
from app.account.repo import AccountRepository
from app.auth.deps import get_current_user
from app.auth.repo import RevokedTokenRepository
from app.auth.services import AuthService
from app.auth.types import CurrentUser
from app.core.constraint_registry import ConstraintRegistry
from app.core.transaction_manager import TransactionManager
from app.payment.models import Payment
from app.payment.repo import PaymentRepository
from app.payment.service import PaymentService
from app.user.models import User
from app.user.repo import UserRepository
from app.user.service import UserService


async def provide_session(
    request: Request,
) -> AsyncSession:
    return request.ctx.session


def setup_dependencies(app: Sanic):
    ext: Extend = app.ext

    ext.add_dependency(
        AsyncSession,
        provide_session,
    )

    ext.add_dependency(
        TransactionManager
    )

    ext.dependency(
        ConstraintRegistry(
            [
                User,
                Account,
                Payment,
            ]
        )
    )

    ext.add_dependency(
        RevokedTokenRepository
    )

    ext.add_dependency(
        UserRepository,
    )

    ext.add_dependency(
        AccountRepository,
    )

    ext.add_dependency(
        PaymentRepository,
    )

    ext.add_dependency(
        PaymentService,
    )

    ext.add_dependency(
        AuthService,
    )

    ext.add_dependency(
        UserService,
    )

    ext.add_dependency(
        CurrentUser,
        get_current_user,
    )