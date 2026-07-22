from dataclasses import dataclass

from app.user.models import User


@dataclass
class CurrentUser:
    user: User


@dataclass
class AdminUser:
    user: User