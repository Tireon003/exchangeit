from src.back.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager


class Database:

    def __init__(self):
        self.aengine = create_async_engine(url=settings.db_url)
        self.asession = async_sessionmaker(self.aengine, expire_on_commit=False)

    @asynccontextmanager
    async def create_async_session(self):
        try:
            async with self.asession() as session:
                yield session
        except Exception as e:
            await session.rollback()
        finally:
            await session.close()
