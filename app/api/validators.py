from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


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
    charity_project = await charity_project_crud.get(charity_project_id,
                                                     session)
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


async def check_project_invested_to_delete(
        project_id: int,
        session: AsyncSession,
) -> int:
    charity_project = await check_charity_project_exists(
        project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_full_amount_to_update(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        project_id, session)
    await check_charity_project_closed(project_id, session)
    if obj_in.name is not None and obj_in.name != charity_project.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        db_project_invested_amount = await (
            charity_project_crud.get_project_invested_amount(
                project_id, session))
        if db_project_invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Нельзя установить требуемую сумму меньше уже вложенной!'
            )
    return charity_project
