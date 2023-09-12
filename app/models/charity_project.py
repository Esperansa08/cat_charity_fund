from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean

from app.core.db import Base


class CharityProject(Base):
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    full_amount = Column(Integer, default=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
