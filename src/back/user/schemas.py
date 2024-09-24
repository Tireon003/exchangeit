from pydantic import BaseModel, Field, PositiveInt, PlainSerializer
from datetime import datetime as dt
from typing import Annotated


from ad.schemas import AdFromDB
from contact.schemas import ContactCardFromDB


class User(BaseModel):
    username: str = Field(max_length=20)
    hashed_password: str


class UserCreate(User):
    pass


class UserLogin(User):
    pass


class UserCreds(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(min_length=8)


class UserUpdate(User):
    pass


class UserFromDB(User):
    id: PositiveInt
    signup_timestamp: Annotated[dt, PlainSerializer(
        lambda val: val.strftime(format="%Y-%m-%d %H:%M:%S"),
        return_type=str)
    ]
    last_activity: Annotated[dt, PlainSerializer(
        lambda val: val.strftime(format="%Y-%m-%d %H:%M:%S"),
        return_type=str)
    ]
    is_active: bool

    class Config:
        from_attributes = True


class UserDBRelFavAds(UserFromDB):
    favorite_ads: list["AdFromDB"] | None


class UserDBRelAds(UserFromDB):
    user_ads: list["AdFromDB"] | None


class UserDBRelContacts(UserFromDB):
    contacts: "ContactCardFromDB"


class UserDBRelsAdsFavContacts(UserDBRelFavAds, UserDBRelAds, UserDBRelContacts):
    pass