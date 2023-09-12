from typing import Optional
from datetime import datetime, timedelta as td
from pydantic import BaseModel, Field, PositiveInt, Extra  # validator,


CREATE_DATE = (datetime.now() + td(minutes=10)).isoformat(timespec='minutes')
CLOSE_DATE = (datetime.now() + td(days=10)).isoformat(timespec='minutes')


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]