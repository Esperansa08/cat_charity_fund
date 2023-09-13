from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false
from sqlalchemy import select

from app.models import CharityProject, Donation


async def investment(
        object_in: Union[CharityProject, Donation],
        session: AsyncSession) -> int:
    db_model = (CharityProject if isinstance(object_in, Donation) else Donation)
    not_invested_objects = await session.execute(
        select(db_model).where(
            db_model.fully_invested == false()).order_by(db_model.create_date))
    not_invested_objects = not_invested_objects.scalars().all()
    available_balance = object_in.full_amount
    if not_invested_objects:
        for not_invested_obj in not_invested_objects:
            free_donation = not_invested_obj.full_amount - not_invested_obj.invested_amount
            if free_donation < available_balance:
                to_invest = free_donation
            else:
                to_invest = available_balance
            not_invested_obj.invested_amount += to_invest
            object_in.invested_amount += to_invest
            available_balance -= to_invest
            if not_invested_obj.full_amount == not_invested_obj.invested_amount:
                await set_full_invested(not_invested_obj)

            if not available_balance:
                await set_full_invested(object_in)
                break
        await session.commit()
        await session.refresh(not_invested_obj)
    return object_in


async def set_full_invested(object: Union[CharityProject, Donation]) -> None:
    object.close_date = datetime.now()
    object.fully_invested = True
