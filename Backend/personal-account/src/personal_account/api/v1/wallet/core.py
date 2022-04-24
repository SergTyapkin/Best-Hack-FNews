from os import stat
from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from .models import (
    CurrencyTopUp,
    CurrencyInDB,
    CurrencyWithdraw,
    ExchangeCurrencies,
    ExternalCurrency,
    CurrencyPublicListWallet,
    CurrencyPublicList,
    ExchangeOperations,
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


async def exchange_currency(
    *,
    username: str,
    exchange_currencies: ExchangeCurrencies,
    db: Session,
):
    user = get_user_by_username(
        username=username,
        db=db,
    )

    try:

        if exchange_currencies.valueTo and exchange_currencies.valueFrom:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You cannot set your own rate :)",
            )

        db_currency_from = (
            db.query(Currency)
            .with_parent(user.wallet)
            .filter(Currency.name == exchange_currencies.nameFrom)
            .first()
        )

        if not db_currency_from:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You don't have such currency for exchange",
            )

        if (
            not exchange_currencies.valueFrom
            and exchange_currencies.valueFrom > db_currency_from.amount
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You don't have enough currency for exchange",
            )

        db_currency_to = (
            db.query(Currency)
            .with_parent(user.wallet)
            .filter(Currency.name == exchange_currencies.nameTo)
            .first()
        )

        all_currencies = await get_all_currencies()
        operations = (
            exchange_currency_from(
                exchange_currencies.nameFrom,
                exchange_currencies.nameTo,
                exchange_currencies.valueFrom,
                all_currencies,
            )
            if exchange_currencies.valueFrom
            else exchange_currency_to(
                exchange_currencies.nameFrom,
                exchange_currencies.nameTo,
                exchange_currencies.valueTo,
                all_currencies,
            )
        )

        if db_currency_from.amount - operations.withdrawFromAmount < 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Not enough money from"
            )

        db_currency_from.amount -= operations.withdrawFromAmount
        db_currency_to.amount += operations.topupToAmount

        db.commit()
    except Exception as exc:
        logger.error(exc)
        db.rollback()


def exchange_currency_from(
    nameFrom: str, nameTo: str, valueFrom: float, all_currencies: CurrencyPublicList
) -> ExchangeOperations:
    operations = ExchangeOperations(
        nameWithdrawFrom=nameFrom,
        nameTopUpTo=nameTo,
        withdrawFromAmount=valueFrom,
    )

    mid_sum_rub = valueFrom

    if nameFrom != "RUB":
        cur_from = next(filter(lambda x: x.name == nameFrom, all_currencies.currencies))
        mid_sum_rub = valueFrom / cur_from.rate

    operations.topupToAmount = mid_sum_rub

    return operations


def exchange_currency_to(
    nameFrom: str,
    nameTo: str,
    valueTo: float,
    all_currencies: CurrencyPublicList,
) -> ExchangeOperations:
    operations = ExchangeOperations(
        nameWithdrawFrom=nameFrom,
        nameTopUpTo=nameTo,
        topupToAmount=valueTo,
    )
    cur_from = next(filter(lambda x: x.name == nameFrom, all_currencies.currencies))

    if nameTo == "RUB":
        operations.withdrawFromAmount = valueTo * cur_from.rate
    elif nameFrom == "RUB":
        operations.withdrawFromAmount = valueTo / cur_from.rate
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return operations
