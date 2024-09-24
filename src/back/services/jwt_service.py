import jwt
import datetime as dt

from config import settings
from auth.exceptions import ExpiredTokenException, InvalidTokenException
from auth.schemas import TokenType


class JwtService:

    ALG = "HS256"
    SECRET = settings.hash_secret

    EXP_ACCESS = 7
    EXP_REFRESH = 30

    @classmethod
    def exp_time(cls, token_type: TokenType):
        if token_type.value == TokenType.access:
            return cls.EXP_ACCESS
        else:
            return cls.EXP_REFRESH

    @classmethod
    def create_token(cls, payload: dict, token_type: TokenType):
        payload.update(
            {
                "type": token_type,
                "exp": dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=cls.exp_time(token_type))
            }
        )
        return jwt.encode(
            payload=payload,
            key=cls.SECRET,
            algorithm=cls.ALG
        )

    @classmethod
    def verify_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, cls.SECRET, algorithms=[cls.ALG])
            if payload["type"] not in TokenType:
                raise InvalidTokenException()
            exp_time = dt.datetime.fromtimestamp(payload["exp"], dt.timezone.utc)
            expired = exp_time < dt.datetime.now(dt.timezone.utc)
            if expired:
                raise ExpiredTokenException()
            else:
                return payload
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
