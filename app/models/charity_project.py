from sqlalchemy import Column, String, Text

from app.models.base import PreBaseCharityDonation


class CharityProject(PreBaseCharityDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
