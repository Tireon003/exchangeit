from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime as dt

from models import AdTable, ContactTable


class User(BaseModel):
    username: str = Field(max_length=20)
    hashed_password: str


class UserCreate(User):
    pass


class UserLogin(User):
    pass


class UserFromDB(User):
    id: PositiveInt
    signup_timestamp: dt
    last_activity: dt
    is_active: bool

    class Config:
        from_attributes = True


class UserDBRelFavAds(UserFromDB):
    favorite_ads: "AdTable"


class UserDBRelAds(UserFromDB):
    user_ads: list["AdTable"]


class UserDBRelContacts(UserFromDB):
    contacts: "ContactTable"
