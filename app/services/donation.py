from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.crud import donation_crud
from app.models import CharityProject, Donation, User


async def get_donation_balance(
        full_amount: int,
        session: AsyncSession,
) -> int:
    """Получение значение не распределенного по проектам и изменение данных
    в незакрытом проекте."""
    charity_project_invested = await session.execute(
        select(CharityProject).where(CharityProject.full_amount > CharityProject.invested_amount))
    charity_project_invested = charity_project_invested.scalars().first()
    #balance = full_amount
    need_donation = 0
    if charity_project_invested is not None:
        need_donation = charity_project_invested.full_amount - charity_project_invested.invested_amount
        if full_amount > need_donation:
            close_date = datetime.now()
            setattr(charity_project_invested, 'close_date', close_date)
            setattr(charity_project_invested, 'invested_amount', charity_project_invested.full_amount)
            setattr(charity_project_invested, 'fully_invested', 1)
        else:
            charity = charity_project_invested.invested_amount + full_amount
            setattr(charity_project_invested, 'invested_amount', charity)
        session.add(charity_project_invested)
        await session.commit()
        await session.refresh(charity_project_invested)
    return need_donation


async def set_donation_invested(
        donation_invested: Donation,
        balance: int,
        session: AsyncSession,
) -> int:
    setattr(donation_invested, 'invested_amount', balance)
    if balance >= donation_invested.full_amount:
        close_date = datetime.now()
        setattr(donation_invested, 'close_date', close_date)
        setattr(donation_invested, 'fully_invested', 1)
    else:
        setattr(donation_invested, 'fully_invested', 0)
    session.add(donation_invested)
    await session.commit()
    await session.refresh(donation_invested)
    return donation_invested