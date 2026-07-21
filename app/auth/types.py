from typing import NewType

from app.user.models import User

CurrentUser = NewType(
    "CurrentUser",
    User,
)

AdminUser = NewType(
    "AdminUser",
    User,
)