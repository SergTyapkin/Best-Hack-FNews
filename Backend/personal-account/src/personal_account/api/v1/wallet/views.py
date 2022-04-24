from typing import Optional

from fastapi import APIRouter, Body, Cookie, Depends, status
from loguru import logger

from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..users.authentication import AuthService, JWTBearer
from .models import CurrencyTopUp, CurrencyPublic

from .core import topup_wallet, withdraw_wallet

wallet_router = APIRouter(prefix="/wallet", tags=["wallet"])


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
