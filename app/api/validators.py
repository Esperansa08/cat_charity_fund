# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.crud import donation_crud
from app.models import CharityProject, Donation, User


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_closed(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        project_id,
        session)
    if charity_project.close_date is None:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_charity_project_invested(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        project_id,
        session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_reservation_intersections(**kwargs) -> None:
    donations = await donation_crud.get_donations_at_the_same_time(**kwargs)
    if donations:
        raise HTTPException(
            status_code=422,
            detail=str(donations)
        )


async def check_donation_before_edit(
        donation_id: int,
        session: AsyncSession,
        user: User,
) -> Donation:
    donation = await donation_crud.get(
        obj_id=donation_id, session=session)
    if not donation:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    if donation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужое пожертвование!'
        )
    return donation


async def check_charity_project_before_post(
        charity_project_id: int,
        session: AsyncSession,
        user: User,
) -> Donation:
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session)
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project