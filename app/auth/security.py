import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Dict
from sanic.exceptions import Unauthorized

from app.core.config import settings

from pwdlib import PasswordHash



def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> Dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except InvalidTokenError:
        raise Unauthorized("Invalid token")



_password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    return _password_hash.verify(
        password,
        hashed_password,
    )