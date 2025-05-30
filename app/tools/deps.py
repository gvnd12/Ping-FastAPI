from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas import User, UserIdentity
from app.core.jwt_manager import _jwt_decode

class PingSecurity(HTTPBearer): ...

bearer_token = PingSecurity()

async def load_from_token(token:HTTPAuthorizationCredentials | str) -> User:
    try:
        payload = _jwt_decode(token.credentials if isinstance(token, HTTPAuthorizationCredentials) else token)
        ctx = payload["context"]["user_type"]

        if ctx=="USER":
            user = await UserIdentity(username=payload["context"]["username"]).get_user_with_username()
            return user

    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None

async def get_current_user(
        token: HTTPAuthorizationCredentials | None = Depends(bearer_token)
) -> User:
    if token:
        user = await load_from_token(token)
        return user