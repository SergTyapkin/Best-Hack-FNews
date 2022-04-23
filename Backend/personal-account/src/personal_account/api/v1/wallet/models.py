from typing import Optional

from pydantic import constr, confloat

from ..base.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class CurrencyBase(CoreModel):
    name: Optional[str]
    amount: Optional[float]

    wallet_id: Optional[int]


class CurrencyTopUp(CoreModel):
    username: int

    name: constr(min_length=1, regex="^[a-zA-Z]+$")
    amount: confloat(ge=0.0)


class CurrencyInDB(IDModelMixin, DateTimeModelMixin, CurrencyBase):
    class Config:
        orm_mode = True


class CurrencyPublic(IDModelMixin, DateTimeModelMixin, CurrencyBase):
    class Config:
        orm_mode = True
