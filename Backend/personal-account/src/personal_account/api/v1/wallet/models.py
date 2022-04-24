from typing import Optional

from pydantic import constr, confloat, BaseModel

from ..base.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class CurrencyBase(CoreModel):
    name: Optional[str]
    amount: Optional[float]


class CurrencyTopUp(CoreModel):
    name: constr(min_length=1, regex="^[a-zA-Z]+$")
    amount: confloat(ge=0.0)


class CurrencyWithdraw(CoreModel):
    name: constr(min_length=1, regex="^[a-zA-Z]+$")
    amount: confloat(ge=0.0)


class CurrencyInDB(IDModelMixin, DateTimeModelMixin, CurrencyBase):
    class Config:
        orm_mode = True


class CurrencyPublic(IDModelMixin, DateTimeModelMixin, CurrencyBase):
    class Config:
        orm_mode = True


class CurrencyPublicListWallet(BaseModel):
    currencies: list[CurrencyPublic]


class ExternalCurrency(BaseModel):
    name: str
    rate: float


class CurrencyPublicList(BaseModel):
    currencies: list[ExternalCurrency]


class ExchangeCurrencies(BaseModel):
    nameFrom: str
    nameTo: str
    valueTo: Optional[float]
    valueFrom: Optional[float]


class ExchangeOperations(BaseModel):
    nameWithdrawFrom: str
    nameTopUpTo: str
    withdrawFromAmount: Optional[float] = 0.0
    topupToAmount: Optional[float] = 0.0
