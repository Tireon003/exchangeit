from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends

from services import JwtService
from .schemas import AccessTokenPayload
from user.schemas import UserCreds

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def validate_token(access_token: Annotated[str, Depends(oauth2_scheme)]):
    payload = JwtService.verify_token(access_token)
    payload_model = AccessTokenPayload(**payload)
    return payload_model


def get_login_form(credentials: Annotated[UserCreds, Depends(OAuth2PasswordRequestForm)]):
    return credentials
