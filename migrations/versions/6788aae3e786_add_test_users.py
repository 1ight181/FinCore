"""add test users

Revision ID: 6788aae3e786
Revises: 82246d206c50
Create Date: 2026-07-22 17:03:16.358433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from build.lib.app.auth.security import hash_password

# revision identifiers, used by Alembic.
revision: str = '6788aae3e786'
down_revision: Union[str, Sequence[str], None] = '82246d206c50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

USER_ID = "11111111-1111-1111-1111-111111111111"
ADMIN_ID = "22222222-2222-2222-2222-222222222222"
ACCOUNT_ID = "33333333-3333-3333-3333-333333333333"

def upgrade() -> None:
    test_admin_pwd_hash = hash_password("admin")
    test_user_pwd_hash = hash_password("user")

    users = sa.table(
        "users",
        sa.column("id", sa.UUID()),
        sa.column("email", sa.String()),
        sa.column("password_hash", sa.String()),
        sa.column("full_name", sa.String()),
        sa.column(
            "user_role",
            sa.Enum(
                "user",
                "admin",
                name="userrole",
            ),
        ),
    )

    accounts = sa.table(
        "accounts",
        sa.column("id", sa.UUID()),
        sa.column("user_id", sa.UUID()),
        sa.column("balance", sa.Numeric()),
    )

    op.bulk_insert(
        users,
        [
            {
                "id": ADMIN_ID,
                "email": "admin@test.com",
                "password_hash": f"{test_admin_pwd_hash}",
                "full_name": "Admin User",
                "user_role": "admin",
            },
            {
                "id": USER_ID,
                "email": "user@test.com",
                "password_hash": f"{test_user_pwd_hash}",
                "full_name": "Regular User",
                "user_role": "user",
            },
        ],
    )

    op.bulk_insert(
        accounts,
        [
            {
                "id": ACCOUNT_ID,
                "user_id": USER_ID,
                "balance": 0.00,
            }
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM accounts WHERE id = :id"
        ).bindparams(id=ACCOUNT_ID)
    )

    op.execute(
        sa.text(
            "DELETE FROM users WHERE id IN (:user_id, :admin_id)"
        ).bindparams(
            user_id=USER_ID,
            admin_id=ADMIN_ID,
        )
    )