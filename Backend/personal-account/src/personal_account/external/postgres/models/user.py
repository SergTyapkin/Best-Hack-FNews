from ast import In
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db import Base

users_news_books = Table(
    "users_news_books",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("news_book_id", Integer, ForeignKey("news_books.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    is_email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)

    wallet = relationship("Wallet", uselist=False, backref="users")
    news_books = relationship("NewsBooks", secondary=users_news_books)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


class NewsBooks(Base):
    __tablename__ = "news_books"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)

    __mapper_args__ = {"eager_defaults": True}
