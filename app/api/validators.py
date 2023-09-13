from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

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
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
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
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_charity_project_invested(
        project_id: int,
        session: AsyncSession,
) -> int:
    project_amount = await charity_project_crud.get_project_invested_amount(
        project_id, session)
    if project_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project_amount


async def check_full_amount_to_update(
        project_id: int,
        full_amount_to_update: PositiveInt,
        session: AsyncSession,
) -> None:
    db_project_invested_amount = await (
        charity_project_crud.get_project_invested_amount(project_id, session))
    if db_project_invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
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
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    if donation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
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
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project
