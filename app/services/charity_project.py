from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.crud import donation_crud
from app.models import CharityProject, Donation, User


async def charity_project_balance(
        full_amount: int,
        session: AsyncSession,
) -> int:
    project_invested = await session.execute(
        select(CharityProject).where(CharityProject.full_amount < CharityProject.invested_amount))
    project_invested = project_invested.scalars().first()
    balance = 0
    if project_invested is not None:
        invested_amount = project_invested.invested_amount - project_invested.full_amount
        project_invested.invested_amount = project_invested.full_amount
        balance = full_amount - invested_amount

        setattr(project_invested, 'invested_amount', project_invested.full_amount)
        session.add(project_invested)
        await session.commit()
        await session.refresh(project_invested)
    return balance


async def charity_project_invested(
        project_invested: CharityProject,
        balance: int,
        session: AsyncSession,
) -> int:
    setattr(project_invested, 'invested_amount', balance)
    session.add(project_invested)
    await session.commit()
    await session.refresh(project_invested)
    return project_invested