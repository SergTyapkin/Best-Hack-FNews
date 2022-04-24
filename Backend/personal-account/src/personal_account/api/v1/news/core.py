from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ..base.utils import get_user_by_username
from ....external.requests.vk import get_newsfeed
from .models import NewsPack, News


async def get_news(*, username: str, db: Session) -> NewsPack:
    user = get_user_by_username(
        username=username,
        db=db,
    )

    news_pack = NewsPack(news=[])

    for book in user.news_books:
        q = book.name
        start_date = datetime.timestamp(datetime.utcnow() - timedelta(days=1))

        newsfeed = await get_newsfeed(q, int(start_date))
        response = newsfeed.get("response", {})
        newsfeed_items = response.get("items", [])

        for news in newsfeed_items:
            prepared_news = {
                "title": news.get("title", ""),
                "description": news.get("text", ""),
                "date": news.get("date", ""),
                "source": "VK",
                "tags": q,
            }

            to_news_pack = News(
                title=prepared_news.get("title"),
                description=prepared_news.get("description"),
                date=prepared_news.get("date"),
                source=prepared_news.get("source"),
                tags=[prepared_news.get("tags")],
            )

            news_pack.news.append(to_news_pack)
    return news_pack
