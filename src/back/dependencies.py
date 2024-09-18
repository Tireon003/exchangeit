from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core import database as db
from services import JwtService
from schemas import AccessTokenPayload, UserCreds

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db.create_async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


def validate_token(access_token: Annotated[str, Depends(oauth2_scheme)]):
    payload = JwtService.verify_token(access_token)
    payload_model = AccessTokenPayload(**payload)
    return payload_model


def get_login_form(credentials: Annotated[UserCreds, Depends(OAuth2PasswordRequestForm)]):
    return credentials
