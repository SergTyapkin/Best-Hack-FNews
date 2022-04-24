from typing import Optional

from pydantic import constr, confloat

from ..base.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class NewsBookBase(CoreModel):
    name: Optional[str]


class NewsBookAdd(CoreModel):
    name: str


class NewsBookInDB(IDModelMixin, DateTimeModelMixin, NewsBookBase):
    class Config:
        orm_mode = True


class NewsBookPublic(IDModelMixin, DateTimeModelMixin, NewsBookBase):
    class Config:
        orm_mode = True
