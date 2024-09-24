from pydantic import BaseModel, Field, PositiveInt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user.schemas import UserFromDB


class ContactCard(BaseModel):
    email: str | None = Field(default=None)
    telegram: str | None = Field(max_length=20, default=None)
    phone_number: PositiveInt | None = Field(default=None)


class ContactCardCreate(ContactCard):
    by_user: int


class ContactCardFromDB(ContactCard):
    id: int

    class Config:
        from_attributes = True


class ContactCardDBRelUser(ContactCardFromDB):
    user: "UserFromDB"
