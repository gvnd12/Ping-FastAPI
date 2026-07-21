import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.schemas import User
from app.tools.deps import get_current_user

logger = logging.getLogger(settings.APP_NAME)

whoami_router = APIRouter(tags=["whoami"], prefix="/api/whoami")


@whoami_router.get("/whoami")
async def whoami(user: Annotated[User, Depends(get_current_user)]):
    try:
        return user
    except Exception as e:
        logger.error(f"Error in whoami: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
