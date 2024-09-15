from .auth import router as auth_router
from .user import router as users_router
from .ads_router import router as ads_router

__all__ = [
    "auth_router",
    "users_router",
    "ads_router",
]