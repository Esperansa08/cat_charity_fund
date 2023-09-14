from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy import CheckConstraint
from app.core.db import Base


class PreBaseCharityDonation(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint("full_amount >= invested_amount", name="full_amount_ge_invested_amount"),
        CheckConstraint("full_amount > 0", name="full_amount_is_positive"))

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, index=True, default=None)

    def __repr__(self):
        return ('Дата создания - {self.create_date}, '
                'Общая сумма - {self.full_amount}, '
                'Инвестировано - {self.invested_amount}, '
                'Дата закрытия - {self.close_date}. ')