from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager


class Database:

    def __init__(self):
        self.aengine = create_async_engine(url=settings.db_url, echo=True)
        self.asession = async_sessionmaker(self.aengine, expire_on_commit=False)

    @asynccontextmanager
    async def create_async_session(self):
        async with self.asession() as session:
            yield session


database = Database()
