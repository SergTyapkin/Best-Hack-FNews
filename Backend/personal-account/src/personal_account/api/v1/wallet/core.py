# from sqlalchemy.orm import Session
# from sqlalchemy.dialects.postgresql import insert

# from .models import CurrencyTopUp
# from ..users.core import get_user_by_username
# from ....external.postgres.models.currency import Currency


# def topup_wallet(*, currency: CurrencyTopUp, db: Session):
#     user = get_user_by_username(
#         username=currency.username,
#         db=db,
#     )
