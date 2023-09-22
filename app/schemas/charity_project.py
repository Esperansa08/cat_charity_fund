from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

MAX_LENGHT = 100


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=MAX_LENGHT)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, max_length=MAX_LENGHT)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid