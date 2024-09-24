from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

from .repository import AdsRepository


def get_ads_repository(get_async_session: Callable):
    def _get_ads_repository(session: AsyncSession = Depends(get_async_session)) -> AdsRepository:
        return AdsRepository(session)

    return _get_ads_repository
