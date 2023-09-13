from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.crud import donation_crud
from app.models import CharityProject, Donation, User
from app.services.donation import set_donation_invested


async def charity_project_balance(
        full_amount: int,
        session: AsyncSession,
) -> int:
    donation_invested = await session.execute(
        select(Donation).where(Donation.full_amount > Donation.invested_amount))
    donation_invested = donation_invested.scalars().first()
    free_donation = 0
    balance = 0
    if donation_invested is not None:
        free_donation = donation_invested.full_amount - donation_invested.invested_amount
        if free_donation > full_amount:
            balance = donation_invested.invested_amount + full_amount
            free_donation = free_donation - full_amount
        else:
            if donation_invested.full_amount > free_donation:
                balance = donation_invested.full_amount
            close_date = datetime.now()
            setattr(donation_invested, 'close_date', close_date)
            setattr(donation_invested, 'fully_invested', 1)
            setattr(donation_invested, 'user_id', 1) #session.user.id)
        setattr(donation_invested, 'invested_amount', balance)
        session.add(donation_invested)
        await session.commit()
        await session.refresh(donation_invested)
    return free_donation


async def set_full_invested(
        project_invested: CharityProject,
        balance: int,
        session: AsyncSession,
) -> int:
    if balance >= project_invested.full_amount:
        close_date = datetime.now()
        setattr(project_invested, 'close_date', close_date)
        setattr(project_invested, 'fully_invested', 1)
        setattr(project_invested, 'invested_amount', project_invested.full_amount)
    else:
        setattr(project_invested, 'fully_invested', 0)
        setattr(project_invested, 'invested_amount', balance)
    session.add(project_invested)
    await session.commit()
    await session.refresh(project_invested)
    return project_invested