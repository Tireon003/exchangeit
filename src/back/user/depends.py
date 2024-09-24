from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

from .repository import UserRepository


def get_user_repository(get_async_session: Callable):
    def _get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
        return UserRepository(session)

    return _get_user_repository
