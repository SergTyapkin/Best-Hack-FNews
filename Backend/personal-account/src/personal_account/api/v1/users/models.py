from typing import Optional
from pydantic import EmailStr, constr

from ..base.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class UserBase(CoreModel):
    username: Optional[str]
    email: Optional[EmailStr]

    wallet_id: Optional[int]

    is_email_verified: bool = False
    is_active: bool = True
    is_staff: bool = False


class UserCreate(CoreModel):
    username: constr(min_length=6, max_length=16, regex="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: constr(
        min_length=8,
        max_length=128,
        regex="^[a-zA-Z0-9~!@#$%^&*='|:\". <>,.? /]+$",
    )


class UserEnter(CoreModel):
    username: str
    password: str


class UserPublicEnter(CoreModel):
    username: str
    email: EmailStr


class UserUpdate(CoreModel):
    username: Optional[
        Optional[constr(min_length=6, max_length=16, regex="^[a-zA-Z0-9_-]+$")]
    ]
    email: Optional[EmailStr]


class UserPasswordUpdate(CoreModel):
    password: constr(
        min_length=8,
        max_length=128,
        regex="^[a-zA-Z0-9~!@#$%^&*='|:\". <>,.? /]+$",
    )
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    password: constr(
        min_length=8,
        max_length=128,
        regex="^[a-zA-Z0-9~!@#$%^&*='|:\". <>,.? /]+$",
    )
    salt: str

    class Config:
        orm_mode = True


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    class Config:
        orm_mode = True
