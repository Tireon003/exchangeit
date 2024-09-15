from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core import database as db


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db.create_async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
