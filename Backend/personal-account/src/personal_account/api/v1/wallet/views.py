from fastapi import APIRouter, Body, Depends, status

from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..users.authentication import AuthService, JWTBearer
from .models import CurrencyTopUp, CurrencyPublic

from .core import topup_wallet

wallet_router = APIRouter(prefix="/wallet", tags=["wallet"])


@wallet_router.post(
    "/topup",
    response_model=CurrencyPublic,
    name="wallet:topup-wallet",
    status_code=status.HTTP_200_OK,
)
async def topup_wallet_view(
    currency: CurrencyTopUp = Body(..., embed=True),
    db: Session = Depends(get_db),
    token: str = Depends(JWTBearer()),
):
    username = AuthService.get_usernameJWT(token)

    topup_data = topup_wallet(
        username=username,
        currency=currency,
        db=db,
    )

    return CurrencyPublic(**topup_data.dict())
