from uuid import uuid4

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, UTC
from typing import Dict
from sanic.exceptions import Unauthorized

from app.core.config import settings

from pwdlib import PasswordHash



def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = settings.access_token_expire_minutes

    expire = datetime.now(UTC) + expires_delta
    jti = str(uuid4())

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "jti": jti
    }

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return token


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