from sqlalchemy.orm import Session

from .models import CurrencyTopUp, CurrencyInDB
from ....external.postgres.models.currency import Currency
from ..base.utils import get_user_by_username


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

    return CurrencyInDB(db_currency.__dict__)
