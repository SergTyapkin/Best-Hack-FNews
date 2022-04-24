from pydantic import BaseModel


class News(BaseModel):
    title: str = ""
    description: str = ""
    date: str = ""
    source: str = ""
    tags: list = []


class NewsPack(BaseModel):
    news: list[News] = []
