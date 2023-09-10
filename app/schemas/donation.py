from typing import Optional
from datetime import datetime, timedelta as td
from pydantic import BaseModel, Extra, root_validator, validator
from pydantic import Field

CREATE_DATE = (datetime.now() + td(minutes=10)).isoformat(timespec='minutes')
CLOSE_DATE = (datetime.now() + td(days=10)).isoformat(timespec='minutes')


class DonationBase(BaseModel):
    full_amount: int
    comment: str

    # comment: str
    # user_id: int  # = Column(Integer, ForeignKey('user.id'))

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    id: int
    create_date: datetime = Field(default=0, example=CREATE_DATE)

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    user_id: int
    invested_amount: int
    fully_invested: int
    close_date: datetime = Field(None, example=CLOSE_DATE)

    class Config:
        orm_mode = True
