from fastapi import APIRouter, Body, Cookie, Depends, status
from loguru import logger

from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..users.authentication import AuthService, JWTBearer
from .models import (
    CurrencyTopUp,
    CurrencyPublic,
    CurrencyPublicListWallet,
    CurrencyPublicList,
    ExchangeCurrencies,
)

from .core import (
    topup_wallet,
    withdraw_wallet,
    get_all_currencies,
    get_all_currencies_in_wallet,
    exchange_currency,
)

wallet_router = APIRouter(prefix="/api/v1/wallet", tags=["wallet"])


@wallet_router.post(
    "/topup",
    response_model=CurrencyPublic,
    name="wallet:topup-wallet",
    status_code=status.HTTP_200_OK,
)
async def topup_wallet_view(
    session: str = Cookie(None),
    currency: CurrencyTopUp = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    JWTBearer.verify_jwt(session)
    username = AuthService.get_usernameJWT(session)

    topup_data = topup_wallet(
        username=username,
        currency=currency,
        db=db,
    )

    return CurrencyPublic(**topup_data.dict())


@wallet_router.post(
    "/withdraw",
    response_model=CurrencyPublic,
    name="wallet:withdraw-wallet",
    status_code=status.HTTP_200_OK,
)
async def withdraw_wallet_view(
    session: str = Cookie(None),
    currency: CurrencyTopUp = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    JWTBearer.verify_jwt(session)
    username = AuthService.get_usernameJWT(session)

    withdraw_data = withdraw_wallet(
        username=username,
        currency=currency,
        db=db,
    )

    return CurrencyPublic(**withdraw_data.dict())


@wallet_router.get(
    "/currencies",
    response_model=CurrencyPublicListWallet,
    name="wallet:get-all-currencies",
    status_code=status.HTTP_200_OK,
)
async def get_all_currencies_in_wallet_view(
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    JWTBearer.verify_jwt(session)
    username = AuthService.get_usernameJWT(session)

    all_currencies = get_all_currencies_in_wallet(
        username=username,
        db=db,
    )

    return all_currencies


@wallet_router.get(
    "/currencies/all",
    response_model=CurrencyPublicList,
    name="wallet:get-all-currencies",
    status_code=status.HTTP_200_OK,
)
async def get_all_currencies_view():
    all_currencies = await get_all_currencies()

    return all_currencies


@wallet_router.post(
    "/exchange",
    # response_model=str,
    name="wallet:exchange-currencies",
    status_code=status.HTTP_200_OK,
)
async def get_all_currencies_view(
    exchange_currencies: ExchangeCurrencies,
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    JWTBearer.verify_jwt(session)
    username = AuthService.get_usernameJWT(session)
    await exchange_currency(
        username=username,
        exchange_currencies=exchange_currencies,
        db=db,
    )

    return {}
