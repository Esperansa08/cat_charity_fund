from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import investment
from app.api.validators import (check_name_duplicate,
                                check_project_invested_to_delete,
                                check_full_amount_to_update)


router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],)
async def create_new_charity_project(
        project_json: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создаёт благотворительный проект."""
    await check_name_duplicate(project_json.name, session)
    new_charity_project = await charity_project_crud.create(
        project_json, session, pass_commit=True)
    session.add_all(
        investment(
            new_charity_project,
            await donation_crud.get_multi_ordered_by_create_date(
                session)))
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)],)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    нельзя установить требуемую сумму меньше уже вложенной."""
    charity_project = await check_full_amount_to_update(
        charity_project_id, obj_in, session)
    return await charity_project_crud.update(
        charity_project, obj_in, session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Удаляет проект.
    Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть."""
    charity_project = await check_project_invested_to_delete(
        charity_project_id, session)
    return await charity_project_crud.remove(
        charity_project, session)
