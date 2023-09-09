from sqlalchemy import Column, String, Text, Boolean, DateTime
from pydantic import PositiveInt
#from sqlalchemy.orm import relationship

from app.core.db import Base
#from app.models.reservation import Reservation


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
