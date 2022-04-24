from re import L
from loguru import logger
from sqlalchemy.orm import Session

from .models import NewsBookAdd, NewsBookInDB
from ....external.postgres.models.user import NewsBooks
from ..base.utils import get_user_by_username


def get_news_book_by_name(*, name: str, db: Session) -> NewsBooks:
    news_book_record = db.query(NewsBooks).filter(NewsBooks.name == name).first()

    if not news_book_record:
        return

    return news_book_record


def add_news_book(
    *, username: str, news_book: NewsBookAdd, db: Session
) -> NewsBookInDB:
    user = get_user_by_username(
        username=username,
        db=db,
    )

    db_news_book = get_news_book_by_name(name=news_book.name, db=db)

    if not db_news_book:
        db_news_book = NewsBooks(name=news_book.name)
        db.add(db_news_book)
        db.commit()

    user.news_books.append(db_news_book)
    db.commit()

    logger.info(db_news_book.id)

    return NewsBookInDB(**db_news_book.__dict__)
