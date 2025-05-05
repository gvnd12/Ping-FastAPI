import json
import uuid
from datetime import UTC, datetime, timedelta
from jose import jwt
from typing import Any
from .config import settings

def _jwt_encode(context:dict, identity:str):
    return jwt.encode(
        claims=context,
        key=str(settings.SECRET_KEY),
        algorithm=settings.JWT_ALGORITHM
    )

def _jwt_decode(token:str):
    return jwt.decode(
        token=token,
        algorithms=settings.JWT_ALGORITHM,
        key=str(settings.SECRET_KEY)
    )