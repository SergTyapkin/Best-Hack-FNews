from fastapi import APIRouter, Cookie, Depends, status

from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..users.authentication import JWTBearer, AuthService

from .core import get_news
from .models import NewsPack

news_router = APIRouter(prefix="/api/v1/news", tags=["news"])


@news_router.get(
    "/",
    # response_model=NewsPack,
    name="news:get-news",
    status_code=status.HTTP_200_OK,
)
async def get_news_view(
    db: Session = Depends(get_db),
    session: str = Cookie(None),
):
    JWTBearer.verify_jwt(session)
    username = AuthService.get_usernameJWT(session)

    news = await get_news(username=username, db=db)
    return news

    # return NewsBookPublic(**news_book.dict())
