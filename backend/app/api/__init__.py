from app.api.admin import admin_router
from app.api.auth import auth_route
from app.api.user import post_route, user_route

__all__ = ["user_route", "auth_route", "admin_router", "post_route"]
