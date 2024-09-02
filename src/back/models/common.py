from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, String, text
from datetime import datetime as dt
from typing import Annotated


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

    favorite_ads: Mapped["AdTable"] = relationship(
        back_populates="in_user_favorites",
        secondary="favorites"
    )

    user_ads: Mapped[list["AdTable"]] = relationship(
        back_populates="belongs_to",
    )

    # user_chats: Mapped[list["AdTable"]] = relationship(
    #     back_populates="chats_with",
    #     secondary="messages"
    # )


class AdTable(Base):
    __tablename__ = "ads"

    id: Mapped[ReusableTypes.intpk]
    by_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"))
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
        back_populates="ads_of_each",
    )

    # chats_with: Mapped[list["UserTable"]] = relationship(
    #     back_populates="user_chats",
    #     secondary="messages"
    # )


class CategoryTable(Base):
    __tablename__ = "categories"

    id: Mapped[ReusableTypes.intpk]
    category_name: Mapped[ReusableTypes.str40]

    ads_of_each: Mapped["AdTable"] = relationship(
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


# class MessageTable(Base):
#     __tablename__ = "messages"
#
#     id: Mapped[int] = mapped_column(unique=True)
#     ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))
#     from_user: Mapped[int] = mapped_column(
#         ForeignKey('users.id', ondelete="CASCADE"),
#         primary_key=True
#     )
#     to_user: Mapped[int] = mapped_column(
#         ForeignKey('users.id', ondelete="CASCADE"),
#         primary_key=True
#     )
#     message: Mapped[ReusableTypes.str300]
#     msg_timestamp: Mapped[ReusableTypes.dt_default_now]
