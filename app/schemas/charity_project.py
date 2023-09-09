#from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt  # validator,


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectDB):
    pass
    # @validator('name')
    # def name_cannot_be_null(cls, value: str):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value