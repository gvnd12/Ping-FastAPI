from datetime import UTC, datetime, timedelta
from jose import jwt
from .config import settings

now = datetime.now(UTC)
expires_delta = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def _jwt_encode(context: dict):
    return jwt.encode(
        claims={"iat": now, "exp": now + expires_delta, "context": context},
        key=str(settings.SECRET_KEY),
        algorithm=settings.JWT_ALGORITHM,
    )


def _jwt_decode(token: str):
    return jwt.decode(
        token=token, algorithms=settings.JWT_ALGORITHM, key=str(settings.SECRET_KEY)
    )
