from core import database as db
from models import UserTable


class Crud:

    @staticmethod
    async def create_user(username: str, hashed_password: str):
        async with db.create_async_session() as session:
            new_user = UserTable(
                username=username,
                hashed_password=hashed_password,
            )
            session.add(new_user)
            await session.commit()
