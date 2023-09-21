from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_project_invested_amount(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> int:
        project_invested_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id
            )
        )
        return project_invested_amount.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        project_fully_invested = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1))
        return sorted(
            project_fully_invested.scalars().all(),
            key=lambda project_fully_invested: (
                project_fully_invested.close_date - project_fully_invested.create_date))


charity_project_crud = CRUDCharityProject(CharityProject)
