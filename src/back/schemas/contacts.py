from pydantic import BaseModel, Field, PositiveInt

from models import UserTable


class ContactCard(BaseModel):
    email: str | None = Field(default=None)
    telegram: str | None = Field(min_length=2, max_length=20, default=None)
    phone_number: PositiveInt | None = Field(default=None)


class ContactCardCreateUpdate(ContactCard):
    pass


class ContactCardFromDB(ContactCard):
    id: PositiveInt
    by_user: PositiveInt

    class Config:
        from_attributes = True


class ContactCardDBRelUser(ContactCardFromDB):
    user: "UserTable"
