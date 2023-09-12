from datetime import datetime
from typing import Optional
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.crud.base import CRUDBase
from app.core.user import current_user
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ):  # -> list[Reservation]:
        pass
    #     select_stmt = select(Reservation).where(
    #         Reservation.meetingroom_id == meetingroom_id,
    #         and_(
    #             from_reserve <= Reservation.to_reserve,
    #             to_reserve >= Reservation.from_reserve)
    #     )
    #     if reservation_id is not None:
    #         # ... то к выражению нужно добавить новое условие.
    #         select_stmt = select_stmt.where(
    #             # id искомых объектов не равны id обновляемого объекта.
    #             Reservation.id != reservation_id
    #         )
    #     # Выполняем запрос.
    #     reservations = await session.execute(select_stmt)
    #     reservations = reservations.scalars().all()
    #     return reservations


donation_crud = CRUDDonation(Donation)
