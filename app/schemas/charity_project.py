#from typing import Optional
from datetime import datetime, timedelta as td
from pydantic import BaseModel, Field, PositiveInt, Extra  # validator,


CREATE_DATE = (datetime.now() + td(minutes=10)).isoformat(timespec='minutes')
CLOSE_DATE = (datetime.now() + td(days=10)).isoformat(timespec='minutes')


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool = Field(default=False)
    create_date: datetime = Field(datetime.now(), example=CREATE_DATE)
    close_date: datetime = Field(None, example=CLOSE_DATE)

    class Config:
        orm_mode = True
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectDB):
    pass
    # @validator('name')
    # def name_cannot_be_null(cls, value: str):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value