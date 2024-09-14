from models import UserTable, ContactTable, AdTable
from schemas import UserCreate, UserUpdate, ContactCardCreate, UserFromDB
from core import database as db
from fastapi_cache.decorator import cache
from sqlalchemy import delete, select


class UserORM:

    @staticmethod
    async def create_user(user_obj: UserCreate) -> UserFromDB:
        async with db.create_async_session() as session:
            new_user = UserTable(**user_obj.model_dump())
            session.add(new_user)
            await session.flush()
            await session.refresh(new_user)
            contacts_model = ContactCardCreate.model_validate(
                {
                    "by_user": new_user.id,
                }
            )
            contact_card = ContactTable(**contacts_model.model_dump())
            session.add(contact_card)
            await session.commit()
            created_user_model = UserFromDB.model_validate(new_user)
            return created_user_model

    @staticmethod
    @cache(expire=60)
    async def select_user_by_id(user_id: int) -> UserFromDB:
        async with db.create_async_session() as session:
            query = select(UserTable).filter_by(id=user_id)
            result = await session.scalars(query)
            user = result.one_or_none()
            if not user:
                return
            user_model = UserFromDB.model_validate(user)
            return user_model

    @staticmethod
    async def select_user_by_username(username: str):
        async with db.create_async_session() as session:
            query = select(UserTable).filter_by(username=username)
            result = await session.scalars(query)
            user = result.one_or_none()
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
