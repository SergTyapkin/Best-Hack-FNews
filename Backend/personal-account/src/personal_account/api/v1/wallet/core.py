from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .models import (
    CurrencyTopUp,
    CurrencyInDB,
    CurrencyWithdraw,
    ExternalCurrency,
    CurrencyPublicListWallet,
    CurrencyPublicList,
)
from ....external.postgres.models.currency import Currency
from ..base.utils import get_user_by_username
from ....external.requests.cbr import get_currencies_rate


def topup_wallet(
    *, username: str, currency: CurrencyTopUp, db: Session
) -> CurrencyInDB:
    user = get_user_by_username(
        username=username,
        db=db,
    )

    db_currency = (
        db.query(Currency)
        .with_parent(user.wallet)
        .filter(Currency.name == currency.name)
        .first()
    )

    if not db_currency:
        db_currency = Currency(
            name=currency.name, amount=currency.amount, wallet_id=user.wallet.id
        )
        db.add(db_currency)
    else:
        db_currency.amount += currency.amount

    db.commit()

    return CurrencyInDB(
        id=db_currency.id, name=db_currency.name, amount=db_currency.amount
    )


def withdraw_wallet(
    *, username: str, currency: CurrencyWithdraw, db: Session
) -> CurrencyInDB:
    user = get_user_by_username(
        username=username,
        db=db,
    )

    db_currency = (
        db.query(Currency)
        .with_parent(user.wallet)
        .filter(Currency.name == currency.name)
        .first()
    )

    if not db_currency:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No such currency in your wallet"
        )
    else:
        if db_currency.amount - currency.amount < 0:
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail="No such currency in your wallet"
            )
        db_currency.amount -= currency.amount

    db.commit()

    return CurrencyInDB(
        id=db_currency.id, name=db_currency.name, amount=db_currency.amount
    )


def get_all_currencies_in_wallet(
    *,
    username: str,
    db: Session,
) -> CurrencyPublicListWallet:
    user = get_user_by_username(
        username=username,
        db=db,
    )

    db_currencies = db.query(Currency).with_parent(user.wallet).all()

    currencies = []

    for currency in db_currencies:
        currencies.append(
            CurrencyInDB(id=currency.id, name=currency.name, amount=currency.amount)
        )

    return CurrencyPublicListWallet(currencies=currencies)


async def get_all_currencies() -> CurrencyPublicList:

    currencies_rate = await get_currencies_rate()
    rates = currencies_rate.get("rates", {})

    currencies = []

    for name, rate in rates.items():
        currencies.append(ExternalCurrency(name=name, rate=rate))

    return CurrencyPublicList(currencies=currencies)
