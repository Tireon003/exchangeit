from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models import UserTable, AdTable, ContactTable, AdsContactsTable, FavoriteTable
from ad.schemas import AdCreate

from .exceptions import UserNotFoundException, AdAlreadyInFavoritesException
from .schemas import UserCreate

from contact.schemas import ContactCardCreate

# todo add redis cache
class UserRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def __repr__(self) -> str:
        """
        Overriding __repr__ for fastapi-cache
        :return:
        """
        return self.__class__.__name__

    async def get_user(self,
                       user_id: int,
                       with_ads: bool = False,
                       with_favorites: bool = False,
                       with_contacts: bool = False) -> UserTable | None:
        stmt = select(UserTable).filter_by(id=user_id)
        if with_ads:
            stmt = stmt.options(selectinload(UserTable.user_ads))
        if with_favorites:
            stmt = stmt.options(selectinload(UserTable.favorite_ads))
        if with_contacts:
            stmt = stmt.options(joinedload(UserTable.contacts))
        result = await self.session.scalars(stmt)
        user = result.one_or_none()
        return user

    async def create_user(self, user: UserCreate) -> int:
        """
        Creates new user and creates his contact record in database
        :param user: user create schema
        :return: id of new user from database
        """
        new_user = UserTable(**user.model_dump())
        self.session.add(new_user)
        await self.session.flush()
        await self.session.refresh(new_user)
        contacts_model = ContactCardCreate.model_validate(
            {
                "by_user": new_user.id,
            }
        )
        contact_card = ContactTable(**contacts_model.model_dump())
        self.session.add(contact_card)
        await self.session.commit()
        return new_user.id

    async def get_contact(self, user_id: int) -> int | None:
        """
        Gets contact id for user.
        :param user_id: user id in database
        :return: contact id from database or None if contact not found
        """
        query = select(ContactTable).filter_by(by_user=user_id)
        result = await self.session.scalars(query)
        contacts = result.one_or_none()
        return contacts.id if contacts else None

    async def create_ad(self, user_id: int,  ad: AdCreate) -> int:
        """
        Creates new ad for user.
        :param user_id: user id in database
        :param ad: ad schema from user
        :return: id of new ad
        """
        ad_dict = ad.model_dump()
        ad_dict.update({'by_user': user_id})
        ad = AdTable(**ad_dict)
        self.session.add(ad)
        await self.session.flush()
        await self.session.refresh(ad)
        contact_id = await self.get_contact(user_id)
        ad_contact_secondary = AdsContactsTable(**{
            "ad_id": ad.id,
            "contact_id": contact_id,
        })
        self.session.add(ad_contact_secondary)
        await self.session.commit()
        return ad.id

    async def get_favorite_ads(self, user_id: int) -> list[AdTable] | None:
        """
        Gets user's favorite ads list.
        :param user_id: user id in database
        :return: list of favorite user ads
        """
        user = await self.get_user(user_id=user_id, with_favorites=True)
        if not user:
            raise UserNotFoundException(user_id)
        user_favorite_ads = user.favorite_ads
        return user_favorite_ads

    async def insert_ad_to_favorite(self, user_id: int, ad_id: int) -> None:
        """
        Inserts ad to user's favorite list.
        :param user_id: user id in database
        :param ad_id: ad id in database
        :return: None
        """
        user_favorites = await self.get_favorite_ads(user_id=user_id)
        for ad in user_favorites:
            if ad.id == ad_id:
                raise AdAlreadyInFavoritesException(ad_id)
        stmt = (
            insert(FavoriteTable)
            .values(
                ad_id=ad_id,
                user_id=user_id
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def remove_ad_from_favorite(self, user_id: int, ad_id: int) -> None:
        """
        Removes ad from user's favorite list.
        :param user_id: user id in database
        :param ad_id: ad id in database
        :return: None
        """
        stmt = (
            delete(FavoriteTable)
            .filter_by(ad_id=ad_id, user_id=user_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_by_username(self, username: str) -> UserTable | None:
        stmt = select(UserTable).filter_by(username=username)
        result = await self.session.scalars(stmt)
        user = result.one_or_none()
        return user

    async  def if_username_exists(self, username: str) -> bool:
        user = self.get_user_by_username(username=username)
        if not user:
            return False
        else:
            return True
