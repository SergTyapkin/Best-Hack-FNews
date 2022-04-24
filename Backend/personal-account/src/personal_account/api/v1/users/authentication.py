from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Request
import bcrypt
import jwt
from passlib.context import CryptContext
from loguru import logger

from .models import UserInDB, UserPasswordUpdate
from .token import JWTCredentials, JWTMeta, JWTPayload
from ....settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    pass


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:

            payload = AuthService.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


class AuthService:
    def create_hashed_password_and_salt(
        self, *, plain_password: str
    ) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plain_password, salt=salt)

        return UserPasswordUpdate(password=hashed_password, salt=salt)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(
        self, *, password: str, salt: str, hashed_password: str
    ) -> bool:
        return pwd_context.verify(password + salt, hashed_password)

    def create_access_token(
        self,
        *,
        user: UserInDB,
        secret_key: str = str(settings.secret_key),
        audience: str = settings.jwt_tokens_aud,
        expires_in: int = settings.token_expires_in_secs
    ) -> str:
        if not user or not isinstance(user, UserInDB):
            return

        jwt_meta = JWTMeta(
            token_intended_for=audience,
            token_issued_at=datetime.timestamp(datetime.utcnow()),
            token_expires_in=datetime.timestamp(
                datetime.utcnow() + timedelta(seconds=expires_in)
            ),
        )

        jwt_credentials = JWTCredentials(
            username=user.username,
            email=user.email,
        )

        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_credentials.dict(),
        )

        access_token = jwt.encode(
            token_payload.dict(),
            secret_key,
            algorithm=settings.jwt_algorithm,
        )

        return access_token

    @staticmethod
    def decodeJWT(token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token,
                str(settings.secret_key),
                algorithms=[settings.jwt_algorithm],
            )
            return (
                decoded_token
                if decoded_token.get("token_expires_in")
                >= datetime.timestamp(datetime.utcnow())
                else None
            )
        except Exception as exc:
            logger.error(exc)
            return {}

    @staticmethod
    def get_usernameJWT(token: str) -> str:
        try:
            decoded_token = jwt.decode(
                token,
                str(settings.secret_key),
                algorithms=[settings.jwt_algorithm],
            )

            return decoded_token.get("username")
        except Exception as exc:
            logger.error(exc)
            return ""
