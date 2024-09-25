from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, String, text, BigInteger
from datetime import datetime as dt
from typing import Annotated
from pydantic import PositiveInt


class ReusableTypes:
    intpk = Annotated[int, mapped_column(primary_key=True)]
    dt_default_now = Annotated[dt, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
    str300 = Annotated[str, mapped_column(String(300))]
    str80 = Annotated[str, mapped_column(String(80))]
    str40 = Annotated[str, mapped_column(String(40))]
    str20 = Annotated[str, mapped_column(String(20))]


class Base(DeclarativeBase):

    def __repr__(self):
        attrs = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__}: {", ".join(attrs)}>"


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[ReusableTypes.intpk]
    username: Mapped[ReusableTypes.str20] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    signup_timestamp: Mapped[ReusableTypes.dt_default_now]
    last_activity: Mapped[ReusableTypes.dt_default_now]
    is_active: Mapped[bool] = mapped_column(default=True)

    favorite_ads: Mapped[list["AdTable"]] = relationship(
        back_populates="in_user_favorites",
        secondary="favorites"
    )

    user_ads: Mapped[list["AdTable"]] = relationship(
        back_populates="belongs_to",
    )

    contacts: Mapped["ContactTable"] = relationship(
        back_populates="user",
    )


class AdTable(Base):
    __tablename__ = "ads"

    id: Mapped[ReusableTypes.intpk]
    by_user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    item_give: Mapped[ReusableTypes.str40]
    item_get: Mapped[ReusableTypes.str40]
    description: Mapped[ReusableTypes.str300]
    location: Mapped[ReusableTypes.str80]
    created_at: Mapped[ReusableTypes.dt_default_now]

    belongs_to: Mapped["UserTable"] = relationship(
        back_populates="user_ads",
    )

    in_user_favorites: Mapped[list["UserTable"]] = relationship(
        back_populates="favorite_ads",
        secondary="favorites"
    )

    ad_category: Mapped["CategoryTable"] = relationship(
        back_populates="ads_in_category",
    )

    ad_contacts: Mapped["ContactTable"] = relationship(
        back_populates="ads_with_contact",
        secondary="ads_contact"
    )


class CategoryTable(Base):
    __tablename__ = "categories"

    id: Mapped[ReusableTypes.intpk]
    category_name: Mapped[ReusableTypes.str40]

    ads_in_category: Mapped["AdTable"] = relationship(
        back_populates="ad_category",
    )


class FavoriteTable(Base):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True
    )
    ad_id: Mapped[int] = mapped_column(
        ForeignKey('ads.id', ondelete="CASCADE"),
        primary_key=True
    )


class ContactTable(Base):
    __tablename__ = "contacts"

    id: Mapped[ReusableTypes.intpk]
    by_user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    email: Mapped[str | None] = mapped_column(default=None)
    telegram: Mapped[ReusableTypes.str20 | None] = mapped_column(default=None)
    phone_number: Mapped[int | None] = mapped_column(BigInteger, default=None)

    user: Mapped["UserTable"] = relationship(
        back_populates="contacts",
    )

    ads_with_contact: Mapped[list["AdTable"]] = relationship(
        back_populates="ad_contacts",
        secondary="ads_contact"
    )


class AdsContactsTable(Base):
    __tablename__ = "ads_contact"

    ad_id: Mapped[int] = mapped_column(
        ForeignKey('ads.id', ondelete="CASCADE"),
        primary_key=True,
    )
    contact_id: Mapped[int] = mapped_column(
        ForeignKey('contacts.id', ondelete="CASCADE"),
        primary_key=True,
    )
