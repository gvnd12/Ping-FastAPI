import logging

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.jwt_manager import jwt_decode
from app.models import UserIdentity

logger = logging.getLogger(settings.APP_NAME)


class PingSecurity(HTTPBearer): ...


bearer_token = PingSecurity()


async def load_from_token(token: HTTPAuthorizationCredentials | str):
    try:
        payload = jwt_decode(
            token.credentials
            if isinstance(token, HTTPAuthorizationCredentials)
            else token
        )
        ctx = payload["context"]["user_type"]

        if ctx == "USER":
            user = await UserIdentity().get_user(
                username=payload["context"]["username"]
            )
            return user
        if ctx == "ADMIN":
            return True

    except Exception as e:
        logger.error(f"User login not valid: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User login not valid!",
        )


async def get_current_user(
    token: HTTPAuthorizationCredentials | None = Depends(bearer_token),
):
    if token:
        user = await load_from_token(token)
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User login not valid!",
    )


async def get_admin(
    token: HTTPAuthorizationCredentials | None = Depends(bearer_token),
):
    if token:
        admin = await load_from_token(token)
        return admin if admin == True else False
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin login not valid!",
    )
