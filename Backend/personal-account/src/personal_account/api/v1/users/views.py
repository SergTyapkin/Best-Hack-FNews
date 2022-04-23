from fastapi import APIRouter, Body, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .models import UserCreate, UserPublic
from ....external.postgres.db_utils import get_db
from .token import AccessToken
from .core import register_new_user, auth_service, authenticate_user
from ....settings import settings

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post(
    "/",
    response_model=UserPublic,
    name="user:register-new-user",
    status_code=status.HTTP_201_CREATED,
)
async def register_new_user_view(
    response: Response,
    new_user: UserCreate = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    created_user = register_new_user(new_user=new_user, db=db)

    access_token = AccessToken(
        access_token=auth_service.create_access_token(user=created_user),
        token_type="Bearer",
    )

    cookie = access_token.access_token

    response.set_cookie(
        key="session-key",
        value=cookie,
        max_age=settings.token_expires_in_secs,
        httponly=True,
    )

    return UserPublic(**created_user.dict())


@user_router.post(
    "/login/token",
    response_model=AccessToken,
    name="user:login-and-password",
)
async def user_login_with_usernames_and_password(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> AccessToken:
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )

    access_token = AccessToken(
        access_token=auth_service.create_access_token(user=user),
        token_type="bearer",
    )

    return access_token
