from datetime import datetime, timedelta as td
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

CREATE_DATE = (datetime.now() + td(minutes=10)).isoformat(timespec='minutes')
CLOSE_DATE = (datetime.now() + td(days=10)).isoformat(timespec='minutes')


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
