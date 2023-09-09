from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base


class Donation(Base):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    # Столбец с внешним ключом: ссылка на таблицу meetingroom.
    #meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))

    # def __repr__(self):
    #     return (
    #         f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
    #     )
