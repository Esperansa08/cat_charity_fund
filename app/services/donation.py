from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.crud import donation_crud
from app.models import CharityProject, Donation, User


async def donation_balance(
        full_amount: int,
        session: AsyncSession,
) -> int:
    charity_project_invested = await session.execute(
        select(CharityProject).where(CharityProject.full_amount > CharityProject.invested_amount))
    charity_project_invested2 = len(charity_project_invested.scalars().all())
    #charity_project_invested1 = charity_project_invested.scalars().first()
    balance = 0
    print(charity_project_invested2) #, charity_project_invested1.name)
   # if charity_project_invested is not None:
        #invested_amount = donation_invested.invested_amount - donation_invested.full_amount
        #charity_project_invested.invested_amount += full_amount
       # balance = charity_project_invested.invested_amount + full_amount
        # setattr(donation_invested, 'invested_amount', donation_invested.full_amount)
        # session.add(donation_invested)
        # await session.commit()
        # await session.refresh(donation_invested)
    return balance


async def donation_invested(
        project_invested: CharityProject,
        balance: int,
        session: AsyncSession,
) -> int:
    setattr(project_invested, 'invested_amount', balance)
    session.add(project_invested)
    await session.commit()
    await session.refresh(project_invested)
    return project_invested