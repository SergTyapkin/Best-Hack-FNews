from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .models import CurrencyTopUp, CurrencyInDB

from ....external.postgres.models.user import User
from ....external.postgres.models.currency import Currency


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


def get_user_by_username(*, username: str, db: Session) -> User:
    user_record = db.query(User).filter(User.username == username).first()

    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
        )

    return user_record
