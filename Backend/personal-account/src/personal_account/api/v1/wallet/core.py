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

#     stmt = insert(Currency).values(wallet_id data="inserted data")
#     stmt = stmt.on_conflict_do_update(
#         index_elements=[my_table.c.user_email],
#         index_where=my_table.c.user_email.like("%@gmail.com"),
#         set_=dict(data=stmt.excluded.data),
#     )
#     conn.execute(stmt)
