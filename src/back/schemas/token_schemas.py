from enum import Enum
from datetime import datetime as dt
from pydantic import BaseModel


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class AccessTokenPayload(BaseModel):
    usr: int
    type: TokenType
    exp: dt
