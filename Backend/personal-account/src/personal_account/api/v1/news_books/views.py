from audioop import add
from fastapi import APIRouter, Body, Depends, status

from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..users.authentication import JWTBearer, AuthService
from .models import NewsBookAdd, NewsBookPublic

from .core import add_news_book

news_books_router = APIRouter(prefix="/api/v1/news-book", tags=["news-book"])


@news_books_router.post(
    "/",
    response_model=NewsBookPublic,
    name="news-book:add-book",
    status_code=status.HTTP_200_OK,
)
async def add_news_book_view(
    news_book_add: NewsBookAdd = Body(..., embed=True),
    db: Session = Depends(get_db),
    token: str = Depends(JWTBearer()),
):
    username = AuthService.get_usernameJWT(token)

    news_book = add_news_book(
        username=username,
        news_book=news_book_add,
        db=db,
    )

    return NewsBookPublic(**news_book.dict())
