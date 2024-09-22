from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import datetime as dt

from fastapi import (
    APIRouter,
    Form,
    status,
    Depends,
    HTTPException,
    Response,
)

from schemas import UserCreate, CreatedResponse, UserExistsResponse, AccessTokenPayload, UserCreds, TokenType
from services import HashingService as HS
from services import JwtService
from orm import UserORM
from exceptions import UserAlreadyExists, InvalidTokenException, ExpiredTokenException, UserNotFoundException
from dependencies import get_async_session, validate_token, get_login_form


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=CreatedResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db_session: AsyncSession = Depends(get_async_session)
):
    user = await UserORM.select_user_by_username(username, db_session)
    if user:
        raise UserAlreadyExists(username)
    else:
        hashed_password = HS.encrypt(password)
        user_schema = UserCreate(**{
            "username": username,
            "hashed_password": hashed_password,
        })
        await UserORM.create_user(user_schema, db_session)
        return CreatedResponse()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    response: Response,
    login_creds: Annotated[UserCreds, Depends(get_login_form)],
    db_session: AsyncSession = Depends(get_async_session)
):
    user_from_db = await UserORM.select_user_by_username(login_creds.username, db_session)
    if not user_from_db:
        raise UserNotFoundException(login_creds.username)
    if not HS.verify(login_creds.password, user_from_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    payload = {
        "usr": user_from_db.id,
        "name": user_from_db.username,
    }
    user_access_token = JwtService.create_token(
        payload=payload,
        token_type=TokenType.access,
    )

    response.set_cookie(
        key="access_token",
        value=user_access_token,
        expires=dt.timedelta(days=7).days * 86400,
        max_age=dt.timedelta(days=7).days * 86400,
    )

    return {
        "access_token": user_access_token,
        "token_type": "Bearer",
    }
