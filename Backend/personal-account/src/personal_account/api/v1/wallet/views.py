from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from .models import CurrencyTopUp, CurrencyPublic

# from .core import topup_wallet


wallet_router = APIRouter(prefix="/wallet", tags=["wallet"])


# @wallet_router.get(
#     "/",
#     response_model=UserPublic,
#     name="wallet:get-currencies",
#     status_code=status.HTTP_201_CREATED,
# )
# async def get_all_currencies_view(
#     new_user: UserCreate = Body(..., embed=True), db: Session = Depends(get_db)
# ):
#     created_user = register_new_user(new_user=new_user, db=db)

#     access_token = AccessToken(
#         access_token=auth_service.create_access_token(user=created_user),
#         token_type="bearer",
#     )

#     return UserPublic(**created_user.dict(), access_token=access_token)


# @wallet_router.post(
#     "/topup",
#     response_model=CurrencyPublic,
#     name="wallet:topup-wallet",
#     status_code=status.HTTP_200_OK,
# )
# async def topup_wallet_view(
#     currency: CurrencyTopUp = Body(..., embed=True), db: Session = Depends(get_db)
# ):
# topup_data = topup_wallet(
#     currency=currency,
#     db=db,
# )

# return CurrencyPublic(**topup_data)
