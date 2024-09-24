from typing import Annotated
import datetime as dt
from fastapi.responses import JSONResponse

from fastapi import (
    APIRouter,
    Form,
    status,
    Depends,
    HTTPException,
    Response,
)

from core import database as db
from services import HashingService as HS
from services import JwtService

from user.schemas import UserCreate, UserCreds
from user.depends import get_user_repository
from user.repository import UserRepository

from .depends import get_login_form
from .schemas import TokenType


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/signup")
async def sign_up(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    user_exists = await user_repository.if_username_exists(username)
    if user_exists:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "msg": "User with such username already exists",
                "username": username,
            }
        )
    else:
        hashed_password = HS.encrypt(password)
        user_schema = UserCreate(**{
            "username": username,
            "hashed_password": hashed_password,
        })
        user_id = await user_repository.create_user(user_schema)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            media_type="application/json",
            content={
                "msg": "User succesfully created",
                "id": user_id,
            }
        )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    login_creds: Annotated[UserCreds, Depends(get_login_form)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    user_exists = await user_repository.if_username_exists(login_creds.username)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with such username does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        user_from_db = await user_repository.get_user_by_username(username=login_creds.username)
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
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            media_type="application/json",
            content={
                "access_token": user_access_token,
                "token_type": "Bearer",
            }
        )
        response.set_cookie(
            key="access_token",
            value=user_access_token,
            expires=dt.timedelta(days=7).days * 86400,
            max_age=dt.timedelta(days=7).days * 86400,
        )
        return response
