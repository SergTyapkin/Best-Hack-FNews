from locale import currency
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    user = Column(Integer, ForeignKey("users.id"))
    currency = relationship("Currency", backref="wallets")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Wallet(id={self.id}, user={self.user.username})"
