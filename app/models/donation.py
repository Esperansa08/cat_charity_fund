from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, Boolean

from app.core.db import Base


class Donation(Base):
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    full_amount = Column(Integer, default=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean)
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
