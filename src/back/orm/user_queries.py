from models import UserTable, ContactTable
from schemas import UserCreate, UserUpdate, ContactCardCreateUpdate
from core import database as db

from sqlalchemy import delete


class UserORM:

    @staticmethod
    async def create_user(user_obj: UserCreate):
        async with db.create_async_session() as session:
            new_user = UserTable(**user_obj.model_dump())
            session.add(new_user)
            await session.flush()
            await session.refresh(new_user)
            contacts_model = ContactCardCreateUpdate.model_validate(
                {
                    "by_user": new_user.id,
                }
            )
            contact_card = ContactTable(**contacts_model.model_dump())
            session.add(contact_card)
            await session.commit()

    @staticmethod
    async def select_user_by_id(user_id: int):
        async with db.create_async_session() as session:
            user = await session.get(UserTable, user_id)
            return user

    @staticmethod
    async def update_user_password(updated_user_obj: UserUpdate):
        async with db.create_async_session() as session:
            user = await session.get(UserTable, updated_user_obj.id)
            user = UserTable(**updated_user_obj.model_dump())
            await session.commit()

    @staticmethod
    async def delete_user(user_id: int):
        async with db.create_async_session() as session:
            query = delete(UserTable).filter_by(id=user_id)
            await session.execute(query)
            await session.commit()
