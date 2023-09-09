from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Extra, root_validator, validator
from pydantic import Field


class DonationBase(BaseModel):
    full_amount: int
    comment: str

    # comment: str
    # user_id: int  # = Column(Integer, ForeignKey('user.id'))

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    id: int
    create_date: datetime


class DonationDB(DonationCreate):
    user_id: int
    invested_amount: int
    fully_invested: int
    close_date: datetime

    class Config:
        orm_mode = True
